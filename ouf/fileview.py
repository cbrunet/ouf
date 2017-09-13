
from PyQt5 import QtCore, QtWidgets

import os
import subprocess
import sys

# TODO: modifiers to open in new window
# TODO: switch icons / tree
# TODO: modify icon size


class FileView(QtWidgets.QTreeView):

    current_path_changed = QtCore.pyqtSignal(str)

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setModel(model)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.activated.connect(self.open_action)

    def open_action(self, index):
        if index.isValid():
            item = index.internalPointer()
            path = index.data(QtCore.Qt.UserRole)
            if item.isDir():
                self.setRootIndex(index)
                self.current_path_changed.emit(path)
            else:
                # TODO: open file / exec process / etc.
                if sys.platform.startswith('linux'):
                    subprocess.run(['xdg-open', path])
                else:
                    os.startfile(path)  # windows
        else:
            # go to root
            self.setRootIndex(index)
            self.current_path_changed.emit("")
