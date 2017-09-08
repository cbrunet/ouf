
from PyQt5 import QtCore, QtWidgets

import os
import subprocess
import sys

# TODO: enter to select / open
# TODO: double-click to open
# TODO: modifiers to open in new window
# TODO: switch icons / tree


class FileView(QtWidgets.QTreeView):

    currentPathChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIconSize(QtCore.QSize(32, 32))
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.doubleClicked.connect(self.openAction)

    def openAction(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item.isDir():
                self.setRootIndex(index)
                self.currentPathChanged.emit(item.path)
            else:
                # TODO: open file / exec process / etc.
                if sys.platform.startswith('linux'):
                    subprocess.run(['xdg-open', item.path])
                else:
                    os.startfile(item.path)  # windows
        else:
            # go to root
            self.setRootIndex(index)
            self.currentPathChanged.emit("")
