
from ouf.filemodel.filemodelitem import FileItemType
from ouf.filemodel.filesystemitem import FileSystemItem

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import os.path


# TODO: show/hide hidden files: use proxy
# TODO: show/hide files
# TODO: icons
# TODO: color symlinks / not readable / hidden
# TODO: handle links
# TODO: read .desktop files!


class FileModel(QtCore.QAbstractItemModel):

    FileItem = {FileItemType.filesystem: FileSystemItem}

    ROOT_PATH = '/'

    def __init__(self, parent=None):
        super().__init__(parent)
        self._files = {}

    def _addItem(self, item_type, path):
        if path not in self._files:
            self._files[path] = self.FileItem[item_type](path)
        return self._files[path]

    def canFetchMore(self, parent):
        if parent.isValid():
            return not parent.internalPointer().isLoaded()
        else:
            return False

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            return index.internalPointer().data(role)

    def fetchMore(self, parent):
        if parent.isValid():
            last = len(parent.internalPointer().path_list) - 1
            self.beginInsertRows(parent, 0, last)
            self.endInsertRows()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def hasChildren(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().isDir()
        else:
            return self.rowCount() > 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return self.tr("Filename")

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid():
            parent_item = parent.internalPointer()
            path = parent_item.childPath(row)
            if path is None:
                # invalid row
                return QtCore.QModelIndex()
            item_type = parent_item.type
            item = self._addItem(item_type, path)
        else:
            item = self._addItem(row, self.ROOT_PATH)
        return self.createIndex(row, column, item)

    def parent(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item.path == self.ROOT_PATH:
                return QtCore.QModelIndex()
            parent_path = os.path.dirname(item.path)
            parent_item = self._addItem(item.type, parent_path)
            row = parent_item.path_list.index(item.path)
            return self.createIndex(row, 0, parent_item)
        return QtCore.QModelIndex()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().rowCount()
        else:
            return 1
            return len(FileItemType)

    def pathIndex(self, path):
        """Create index from path

        TODO: move to filesystemitem?

        """
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return QtCore.QModelIndex()

        if path == self.ROOT_PATH:
            return self.index(0, 0)

        item = self._addItem(FileItemType.filesystem, path)
        parent_item = self._addItem(FileItemType.filesystem, os.path.dirname(path))
        row = parent_item.path_list.index(path)
        return self.createIndex(row, 0, item)
