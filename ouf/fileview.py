
from PyQt5 import QtCore, QtWidgets


# TODO: enter to select / open
# TODO: double-click to open
# TODO: modifiers to open in new window


class FileView(QtWidgets.QTreeView):

    currentPathChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIconSize(QtCore.QSize(32, 32))

        self.doubleClicked.connect(self.openAction)

    def openAction(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item.isDir():
                self.setRootIndex(index)
                self.currentPathChanged.emit(item.path)
            else:
                pass  # TODO: open file / exec process / etc.
        else:
            # go to root
            self.setRootIndex(index)
            self.currentPathChanged.emit("")
