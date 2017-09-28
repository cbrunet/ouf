import os.path
from enum import IntEnum

import natsort as ns
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt

from ouf.filemodel import SortRole


class FileItemType(IntEnum):

    filesystem = 0
    calendar = 1
    category = 2
    favorite = 3


class FileModelItem(QtCore.QObject):

    def __init__(self, type, path, parent=None):
        super().__init__(parent)

        self.type = type
        self.path = path

        self._path_list = None
        self._alphanum = ns.natsort_key(os.path.basename(path), alg=ns.I|ns.LA|ns.IC) if path else ''

    @property
    def path_list(self):
        if self._path_list is None:
            self._path_list = self.fetchPathList()
        return self._path_list

    def append(self, filename):
        if filename not in self.path_list:
            self.path_list.append(filename)

    def childPath(self, row):
        try:
            return self.path_list[row]
        except IndexError:
            return None

    def data(self, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return os.path.basename(self.path)

        if role == Qt.DecorationRole:
            return self.getIcon()

        if role == Qt.UserRole:
            return self.path

        if role == SortRole:
            return self._alphanum

    def isLoaded(self):
        return self._path_list is not None

    def rowCount(self):
        if self.isLoaded():
            return len(self.path_list)
        else:
            return 0

    def isRoot(self):
        return self.path == '/'

    def getIcon(self):
        # if self.isRoot():
        #     return QtGui.QIcon.fromTheme('start-here')

        if self.isHome():
            return QtGui.QIcon.fromTheme('user-home')

        # if self.isDesktop():
        #     return QtGui.QIcon.fromTheme('user-desktop')

        if self.isDir():
            return QtGui.QIcon.fromTheme('folder')  # TODO: add fallback

        # if self.isExecutable():
        #     return QtGui.QIcon.fromTheme('application-x-executable')

        return QtGui.QIcon.fromTheme('text-x-generic')

