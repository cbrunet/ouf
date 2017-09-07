

from ouf.filemodel.filemodelitem import FileModelItem, FileItemType

from PyQt5.QtCore import Qt

import os
from pathlib import Path
import stat


class FileSystemItem(FileModelItem):

    def __init__(self, path, parent=None):
        super().__init__(FileItemType.filesystem, path, parent)
        self._stat = os.lstat(self.path)

    def data(self, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if self.isRoot():
                return self.tr("File System")
        return super().data(role)

    def fetchPathList(self):
        if self.isDir():
            try:
                return list(os.path.join(self.path, f) for f in sorted(os.listdir(self.path)))
            except PermissionError:
                pass
        return []

    def isDir(self):
        return stat.S_ISDIR(self._stat.st_mode)

    def isHome(self):
        return Path(self.path) == Path.home()

    def isExecutable(self):
        return stat.S_IXUSR & self._stat.st_mode
