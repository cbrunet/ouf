

from ouf.filemodel.filemodelitem import FileModelItem, FileItemType

from PyQt5.QtCore import Qt

import os
import stat


class FileSystemItem(FileModelItem):

    def __init__(self, path, parent=None):
        super().__init__(FileItemType.filesystem, path, parent)
        try:
            self._stat = os.stat(self.path)
        except FileNotFoundError:
            self._stat = None
        self._is_link = os.path.islink(self.path)

    def data(self, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self.isRoot():
                return _("File System")
        if role == Qt.UserRole:
            if self.isLink():
                return os.path.join(os.path.dirname(self.path), os.readlink(self.path))
        return super().data(role)

    def fetchPathList(self):
        if self.isDir():
            try:
                return list(os.path.join(self.path, f) for f in sorted(os.listdir(self.path)))
            except PermissionError:
                pass
        return []

    def isDir(self):
        return self._stat is not None and stat.S_ISDIR(self._stat.st_mode)

    def isLink(self):
        return self._is_link

    def isHome(self):
        return self.path == os.path.expanduser('~')

    def isExecutable(self):
        return os.access(self.path, os.X_OK)
