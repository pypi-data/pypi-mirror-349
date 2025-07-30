"""
SFTP based backend implementation - on a sftp server, use files in directories below a base path.
"""

from pathlib import Path
import random
import re
import stat
from typing import Optional

try:
    import paramiko
except ImportError:
    paramiko = None

from ._base import BackendBase, ItemInfo, validate_name
from .errors import BackendError, BackendMustBeOpen, BackendMustNotBeOpen, BackendDoesNotExist, BackendAlreadyExists
from .errors import ObjectNotFound
from ..constants import TMP_SUFFIX


def get_sftp_backend(url):
    # sftp://username@hostname:22/path
    # note:
    # - username and port optional
    # - host must be a hostname (not IP)
    # - must give a path, default is a relative path (usually relative to user's home dir -
    #   this is so that the sftp server admin can move stuff around without the user needing to know).
    # - giving an absolute path is also possible: sftp://username@hostname:22//home/username/borgstore
    sftp_regex = r"""
        sftp://
        ((?P<username>[^@]+)@)?
        (?P<hostname>([^:/]+))(?::(?P<port>\d+))?/  # slash as separator, not part of the path
        (?P<path>(.+))  # path may or may not start with a slash, must not be empty
    """
    if paramiko is not None:
        m = re.match(sftp_regex, url, re.VERBOSE)
        if m:
            return Sftp(username=m["username"], hostname=m["hostname"], port=int(m["port"] or "0"), path=m["path"])


class Sftp(BackendBase):
    # Sftp implementation supports precreate = True as well as = False.
    precreate_dirs: bool = False

    def __init__(self, hostname: str, path: str, port: int = 0, username: Optional[str] = None):
        self.username = username
        self.hostname = hostname
        self.port = port
        self.base_path = path
        self.opened = False
        if paramiko is None:
            raise BackendError("sftp backend unavailable: could not import paramiko!")

    def _get_host_config_from_file(self, path: str, hostname: str):
        """lookup the configuration for hostname in path (ssh config file)"""
        config_path = Path(path).expanduser()
        try:
            ssh_config = paramiko.SSHConfig.from_path(config_path)
        except FileNotFoundError:
            return paramiko.SSHConfigDict()  # empty dict
        else:
            return ssh_config.lookup(hostname)

    def _get_host_config(self):
        """assemble all given and configured host config values"""
        host_config = paramiko.SSHConfigDict()
        # self.hostname might be an alias/shortcut (with real hostname given in configuration),
        # but there might be also nothing in the configs at all for self.hostname:
        host_config["hostname"] = self.hostname
        # first process system-wide ssh config, then override with user ssh config:
        host_config.update(self._get_host_config_from_file("/etc/ssh/ssh_config", self.hostname))
        # note: no support yet for /etc/ssh/ssh_config.d/*
        host_config.update(self._get_host_config_from_file("~/.ssh/config", self.hostname))
        # now override configured values with given values
        if self.username is not None:
            host_config.update({"user": self.username})
        if self.port != 0:
            host_config.update({"port": self.port})
        # make sure port is present and is an int
        host_config["port"] = int(host_config.get("port") or 22)
        return host_config

    def _connect(self):
        ssh = paramiko.SSHClient()
        # note: we do not deal with unknown hosts and ssh.set_missing_host_key_policy here,
        # the user shall just make "first contact" to any new host using ssh or sftp cli command
        # and interactively verify remote host fingerprints.
        ssh.load_system_host_keys()  # this is documented to load the USER's known_hosts file
        host_config = self._get_host_config()
        ssh.connect(
            hostname=host_config["hostname"],
            username=host_config.get("user"),  # if None, paramiko will use current user
            port=host_config["port"],
            key_filename=host_config.get("identityfile"),  # list of keys, ~ is already expanded
            allow_agent=True,
        )
        self.client = ssh.open_sftp()

    def _disconnect(self):
        self.client.close()
        self.client = None

    def create(self):
        if self.opened:
            raise BackendMustNotBeOpen()
        self._connect()
        try:
            # we accept an already existing empty directory and we also optionally create
            # any missing parent dirs. the latter is important for repository hosters that
            # only offer limited access to their storage (e.g. only via borg/borgstore).
            # also, it is simpler than requiring users to create parent dirs separately.
            self._mkdir(self.base_path, exist_ok=True, parents=True)
            # avoid that users create a mess by using non-empty directories:
            contents = list(self.client.listdir(self.base_path))
            if contents:
                raise BackendAlreadyExists(f"sftp storage base path is not empty: {self.base_path}")
        except IOError as err:
            raise BackendError(f"sftp storage I/O error: {err}")
        finally:
            self._disconnect()

    def destroy(self):
        def delete_recursive(path):
            parent = Path(path)
            for child_st in self.client.listdir_attr(str(parent)):
                child = parent / child_st.filename
                if stat.S_ISDIR(child_st.st_mode):
                    delete_recursive(child)
                else:
                    self.client.unlink(str(child))
            self.client.rmdir(str(parent))

        if self.opened:
            raise BackendMustNotBeOpen()
        self._connect()
        try:
            delete_recursive(self.base_path)
        except FileNotFoundError:
            raise BackendDoesNotExist(f"sftp storage base path does not exist: {self.base_path}")
        finally:
            self._disconnect()

    def open(self):
        if self.opened:
            raise BackendMustNotBeOpen()
        self._connect()
        try:
            st = self.client.stat(self.base_path)  # check if this storage exists, fail early if not.
        except FileNotFoundError:
            raise BackendDoesNotExist(f"sftp storage base path does not exist: {self.base_path}") from None
        if not stat.S_ISDIR(st.st_mode):
            raise BackendDoesNotExist(f"sftp storage base path is not a directory: {self.base_path}")
        self.client.chdir(self.base_path)  # this sets the cwd we work in!
        self.opened = True

    def close(self):
        if not self.opened:
            raise BackendMustBeOpen()
        self._disconnect()
        self.opened = False

    def _mkdir(self, name, *, parents=False, exist_ok=False):
        # Path.mkdir, but via sftp
        p = Path(name)
        try:
            self.client.mkdir(str(p))
        except FileNotFoundError:
            # the parent dir is missing
            if not parents:
                raise
            # first create parent dir(s), recursively:
            self._mkdir(p.parents[0], parents=parents, exist_ok=exist_ok)
            # then retry:
            self.client.mkdir(str(p))
        except OSError:
            # maybe p already existed?
            if not exist_ok:
                raise

    def mkdir(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        self._mkdir(name, parents=True, exist_ok=True)

    def rmdir(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        try:
            self.client.rmdir(name)
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def info(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        try:
            st = self.client.stat(name)
        except FileNotFoundError:
            return ItemInfo(name=name, exists=False, directory=False, size=0)
        else:
            is_dir = stat.S_ISDIR(st.st_mode)
            return ItemInfo(name=name, exists=True, directory=is_dir, size=st.st_size)

    def load(self, name, *, size=None, offset=0):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        try:
            with self.client.open(name) as f:
                f.seek(offset)
                f.prefetch(size)  # speeds up the following read() significantly!
                return f.read(size)
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def store(self, name, value):
        def _write_to_tmpfile():
            with self.client.open(tmp_name, mode="w") as f:
                f.set_pipelined(True)  # speeds up the following write() significantly!
                f.write(value)

        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        tmp_dir = Path(name).parent
        # write to a differently named temp file in same directory first,
        # so the store never sees partially written data.
        tmp_name = str(tmp_dir / ("".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8)) + TMP_SUFFIX))
        try:
            # try to do it quickly, not doing the mkdir. each sftp op might be slow due to latency.
            # this will frequently succeed, because the dir is already there.
            _write_to_tmpfile()
        except FileNotFoundError:
            # retry, create potentially missing dirs first. this covers these cases:
            # - either the dirs were not precreated
            # - a previously existing directory was "lost" in the filesystem
            self._mkdir(str(tmp_dir), parents=True, exist_ok=True)
            _write_to_tmpfile()
        # rename it to the final name:
        try:
            self.client.posix_rename(tmp_name, name)
        except OSError:
            self.client.unlink(tmp_name)
            raise

    def delete(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        try:
            self.client.unlink(name)
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def move(self, curr_name, new_name):
        def _rename_to_new_name():
            self.client.posix_rename(curr_name, new_name)

        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(curr_name)
        validate_name(new_name)
        parent_dir = Path(new_name).parent
        try:
            # try to do it quickly, not doing the mkdir. each sftp op might be slow due to latency.
            # this will frequently succeed, because the dir is already there.
            _rename_to_new_name()
        except FileNotFoundError:
            # retry, create potentially missing dirs first. this covers these cases:
            # - either the dirs were not precreated
            # - a previously existing directory was "lost" in the filesystem
            self._mkdir(str(parent_dir), parents=True, exist_ok=True)
            try:
                _rename_to_new_name()
            except FileNotFoundError:
                raise ObjectNotFound(curr_name) from None

    def list(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        validate_name(name)
        try:
            infos = self.client.listdir_attr(name)
        except FileNotFoundError:
            raise ObjectNotFound(name) from None
        else:
            for info in sorted(infos, key=lambda i: i.filename):
                if not info.filename.endswith(TMP_SUFFIX):
                    is_dir = stat.S_ISDIR(info.st_mode)
                    yield ItemInfo(name=info.filename, exists=True, size=info.st_size, directory=is_dir)
