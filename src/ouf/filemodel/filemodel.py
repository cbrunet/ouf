import os.path
import shutil

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from ouf.filemodel.filemodelitem import FileItemType
from ouf.filemodel.filesystemitem import FileSystemItem


# TODO: icons
# TODO: color symlinks / not readable / hidden
# TODO: read .desktop files!
# TODO: columns: mime, moddate, size, permissions, (crdate, user, group, hardlinks)


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

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole and index.column() == 0:
            # Rename file
            path = index.data(Qt.UserRole)
            newpath = os.path.join(os.path.dirname(path), value)
            if os.path.exists(newpath):
                return False

            try:
                os.rename(path, newpath)
            except OSError:
                return False

            parent = index.parent().internalPointer()
            parent.path_list[index.row()] = newpath
            item = index.internalPointer()
            item.path = newpath
            self._files[newpath] = item
            del self._files[path]

            self.dataChanged.emit(index, index)
            return True
        return False

    def fetchMore(self, parent):
        if parent.isValid():
            last = len(parent.internalPointer().path_list) - 1
            self.beginInsertRows(parent, 0, last)
            self.endInsertRows()

    def flags(self, index):
        f = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled
        if index.column() == 0:  # and is editable...
            f |= Qt.ItemIsEditable
        item = index.internalPointer()
        if item.isDir():
            f |= Qt.ItemIsDropEnabled
        else:
            f |= Qt.ItemNeverHasChildren
        return f

    def hasChildren(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            parent_item = parent.internalPointer()
            if not parent_item.isLoaded():
                return parent_item.isDir()
        return self.rowCount() > 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return _("Filename")

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
            try:
                row = parent_item.path_list.index(item.path)
            except ValueError:
                return QtCore.QModelIndex()
            return self.createIndex(row, 0, parent_item)
        return QtCore.QModelIndex()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().rowCount()
        else:
            return 1
            return len(FileItemType)

    def mimeTypes(self):
        return ["text/uri-list"]

    def mimeData(self, indexes):
        data = QtCore.QMimeData()
        data.setUrls([QtCore.QUrl.fromLocalFile(index.data(Qt.UserRole)) for index in indexes])
        return data

    def supportedDragActions(self):
        return Qt.CopyAction | Qt.MoveAction | Qt.LinkAction

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction | Qt.LinkAction

    def canDropMimeData(self, data, action, row, column, parent):
        return True

    def _move_file(self, source, dest_index):
        source_dir, filename = os.path.split(source)
        dest_dir = dest_index.data(Qt.UserRole)
        if source_dir == dest_dir:
            return

        dest_path = os.path.join(dest_dir, filename)
        if os.path.exists(dest_path):
            # TODO: handle name conflicts
            return

        source_index = self.pathIndex(source)
        self.beginMoveRows(source_index.parent(), source_index.row(), source_index.row(),
                           dest_index, self.rowCount(dest_index))

        item = source_index.internalPointer()
        item.path = dest_path
        del self._files[source]
        self._files[dest_path] = item

        del self._files[source_dir].path_list[source_index.row()]
        self._files[dest_dir].append(filename)

        os.rename(source, dest_path)
        self.endMoveRows()

    def _copy_file(self, source, dest):
        print("copy {} to {}".format(source, dest))

    def _link_file(self, source, dest):
        pass

    def dropMimeData(self, data, action, row, column, parent):
        destination_index = self.index(row, column, parent)

        if action == Qt.MoveAction:
            do_action = self._move_file
        elif action == Qt.CopyAction:
            do_action = self._copy_file
        elif action == Qt.LinkAction:
            do_action = self._link_file
        else:
            return False

        for url in data.urls():
            path = url.toLocalFile()
            if path:
                do_action(path, destination_index)

        return True

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

    def create_new_directory(self, path):
        i = 0
        folder_name = os.path.join(path, _("New Folder"))
        while os.path.exists(folder_name):
            i += 1
            folder_name = os.path.join(path, _("New Folder ({})").format(i))

        parent_index = self.pathIndex(path)

        row = self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row, row)
        os.mkdir(folder_name)
        parent = parent_index.internalPointer()
        item = self._addItem(FileItemType.filesystem, folder_name)
        parent.append(folder_name)
        self.endInsertRows()

        return self.createIndex(row, 0, item)

    def delete_files(self, indexes):
        #TODO: undo / redo
        #TODO: trash handling

        paths = [index.data(Qt.UserRole) for index in indexes if index.isValid()]
        for path in paths:
            if path == self.ROOT_PATH:
                continue

            item = self._addItem(FileItemType.filesystem, path)
            parent = self._addItem(FileItemType.filesystem, os.path.dirname(path))
            parent_index = self.pathIndex(parent.path)
            row = parent.path_list.index(path)

            self.beginRemoveRows(parent_index, row, row)
            del parent.path_list[row]
            # del self._files[path]
            if item.isDir():
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.endRemoveRows()