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
            if role == Qt.DisplayRole or role == SortRole:
                return self.mimetype

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
