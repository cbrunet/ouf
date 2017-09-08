
from PyQt5 import QtCore, QtGui, QtWidgets

import os.path


# TODO: back and forth buttons (history)


class PathView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.up_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-up'), self.tr("Parent Directory"), self)
        self.up_action.setEnabled(False)
        self.up_action.setShortcuts(QtGui.QKeySequence(self.tr("Ctrl+Up")))
        self.up_action.triggered.connect(self.goUp)

        self.up_button = QtWidgets.QToolButton()
        self.up_button.setDefaultAction(self.up_action)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.editingFinished.connect(self.setPath)
        # TODO: add validator to normalize path, resolve home, etc.

        layout.addWidget(self.up_button)
        layout.addWidget(self.path_edit)
        self.setLayout(layout)

    def setView(self, view):
        self._view = view
        view.currentPathChanged.connect(self.updatePath)

    def setPath(self, path=None):
        if path is None:
            path = self.path_edit.text()
        index = self._view.model().pathIndex(path)
        if index.isValid() or not path:
            self._view.openAction(index)

    def goUp(self):
        index = self._view.rootIndex()
        if index.isValid():
            path = index.data(QtCore.Qt.UserRole)
            if path == '/':
                self.setPath('')
            else:
                self.setPath(os.path.dirname(path))

    def updatePath(self, path):
        self.path_edit.setText(path)
        # TODO: custom widget with icon, dropdown, etc.
        self.up_action.setEnabled(bool(path))