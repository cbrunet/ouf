from enum import IntEnum
import natsort as ns
import mimetypes
import os
import os.path
import stat

from PyQt5.QtCore import Qt

from ouf.filemodel import SortRole
from ouf.iconfactory import icon_factory
from ouf.util import humanize


class FileItemType(IntEnum):
    filesystem = 0
    # calendar = 1
    # category = 2
    # favorite = 3


class Column(IntEnum):
    name = 0
    size = 1
    mimetype = 2
    permissions = 3


class FileModelItem(object):

    def __init__(self, itemtype, path):
        self.itemtype = itemtype
        self.path = path

        self._path_list = None
        self._alphanum = ns.natsort_key(os.path.basename(path), alg=ns.I | ns.LA | ns.IC) if path else ''
        self._mimetype = None

        try:
            self._stat = os.stat(self.path)
        except FileNotFoundError:
            self._stat = None

    def fetch_path_list(self):
        if self.is_dir:
            try:
                return list(os.path.join(self.path, f) for f in sorted(os.listdir(self.path)))
            except PermissionError:
                pass
            except FileNotFoundError:
                pass
        return []

    def append(self, filename):
        if filename not in self.path_list:
            self.path_list.append(filename)

    def child_path(self, row):
        try:
            return self.path_list[row]
        except IndexError:
            return None

    @property
    def loaded(self):
        return self._path_list is not None

    @property
    def path_list(self):
        if self._path_list is None:
            self._path_list = self.fetch_path_list()
        return self._path_list

    def data(self, column, role=Qt.DisplayRole):
        if column == Column.name:
            if role == Qt.DisplayRole:
                return os.path.basename(self.path)

            if role == Qt.DecorationRole:
                return icon_factory(self)

            if role == Qt.UserRole:
                if self.is_link:
                    return os.path.join(os.path.dirname(self.path), os.readlink(self.path))
                return self.path

            if role == SortRole:
                return self._alphanum

        elif column == Column.size:
            if role == Qt.DisplayRole:
                if self.is_dir:
                    if self.loaded:
                        n = len(self.path_list)
                        return ngettext("{} file", "{} files", n).format(n)
                    return ""
                else:
                    return humanize(self._stat[stat.ST_SIZE]) if self._stat else _("Unknown")

            elif role == SortRole:
                if self.is_dir:
                    if self.loaded:
                        return "D", len(self.path_list)
                    else:
                        return "D", 0
                else:
                    if self._stat:
                        return "F", self._stat[stat.ST_SIZE]
                    else:
                        return "F", 0

        elif column == Column.mimetype:
            if role in (Qt.DisplayRole, SortRole):
                return self.mimetype

        elif column == Column.permissions:
            if role in (Qt.DisplayRole, SortRole):
                return self.permissions_string

    def __len__(self):
        return len(self.path_list) if self.loaded else 0

    @property
    def is_dir(self):
        return self._stat is not None and stat.S_ISDIR(self._stat.st_mode)

    @property
    def is_executable(self):
        return os.access(self.path, os.X_OK)

    @property
    def is_home(self):
        return self.path == os.path.expanduser('~')

    @property
    def is_link(self):
        return self._stat is not None and stat.S_ISLNK(self._stat.st_mode)

    @property
    def is_root(self):
        return self.path == '/'

    @property
    def mimetype(self):
        if self._mimetype is None:
            if self.is_dir:
                self._mimetype = "inode/directory"
            else:
                self._mimetype, encoding = mimetypes.guess_type(self.path, strict=False)
                if self._mimetype is None:
                    self._mimetype = ""
        return self._mimetype

    @property
    def permissions_string(self):
        permissions = ["-" for _ in range(10)]
        if self._stat is not None:
            mode = self._stat[stat.ST_MODE]
            if stat.S_ISSOCK(mode):
                permissions[0] = "s"
            elif stat.S_ISLNK(mode):
                permissions[0] = "l"
            elif stat.S_ISREG(mode):
                permissions[0] = "-"
            elif stat.S_ISBLK(mode):
                permissions[0] = "b"
            elif stat.S_ISDIR(mode):
                permissions[0] = "d"
            elif stat.S_ISCHR(mode):
                permissions[0] = "c"
            elif stat.S_ISFIFO(mode):
                permissions[0] = "f"

            if mode & stat.S_IRUSR:
                permissions[1] = 'r'
            if mode & stat.S_IWUSR:
                permissions[2] = 'w'
            if mode & stat.S_IXUSR:
                if mode & stat.S_ISUID:
                    permissions[3] = 's'
                else:
                    permissions[3] = 'x'
            elif mode & stat.S_ISUID:
                permissions[3] = 'S'

            if mode & stat.S_IRGRP:
                permissions[4] = 'r'
            if mode & stat.S_IWGRP:
                permissions[5] = 'w'
            if mode & stat.S_IXGRP:
                if mode & stat.S_ISGID:
                    permissions[6] = 's'
                else:
                    permissions[6] = 'x'
            elif mode & stat.S_ISGID:
                permissions[6] = 'S'

            if mode & stat.S_IROTH:
                permissions[7] = 'r'
            if mode & stat.S_IWOTH:
                permissions[8] = 'w'
            if mode & stat.S_IXOTH:
                if mode & stat.S_ISVTX:
                    permissions[9] = 't'
                else:
                    permissions[9] = 'x'
            elif mode & stat.S_ISVTX:
                permissions[9] = 'T'

        return "".join(permissions)
