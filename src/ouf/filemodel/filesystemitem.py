from PyQt5.QtCore import Qt

from ouf.filemodel.filemodelitem import FileModelItem, FileItemType


class FileSystemItem(FileModelItem):

    def __init__(self, path):
        super().__init__(FileItemType.filesystem, path)

    def data(self, column, role=Qt.DisplayRole):
        if column == 0:
            if role == Qt.DisplayRole:
                if self.is_root:
                    return _("File System")
        return super().data(column, role)
