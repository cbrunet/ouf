from ouf import shortcuts

from PyQt5 import QtCore, QtGui, QtWidgets

import os.path


# TODO: back and forth buttons (history)
# TODO: location icon


class PathView(QtWidgets.QWidget):

    def __init__(self, path, view, parent=None):
        super().__init__(parent)

        self._create_actions()
        self._create_layout()

        self._view = view
        view.current_path_changed.connect(self.update_path)

        self.go_to(path)

    def _create_actions(self):
        self.up_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-up'), _("Parent Directory"), self)
        self.up_action.setEnabled(False)
        self.up_action.setShortcuts(shortcuts.go_up)
        self.up_action.triggered.connect(self.go_up)

        self.home_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-home'), _("Home"), self)
        self.home_action.setShortcuts(shortcuts.go_home)
        self.home_action.triggered.connect(self.go_home)

    def _create_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.up_button = QtWidgets.QToolButton()
        self.up_button.setDefaultAction(self.up_action)

        self.home_button = QtWidgets.QToolButton()
        self.home_button.setDefaultAction(self.home_action)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.editingFinished.connect(self.go_to)
        # TODO: add validator to normalize path, resolve home, etc.

        layout.addWidget(self.home_button)
        layout.addWidget(self.up_button)
        layout.addWidget(self.path_edit)
        self.setLayout(layout)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        path = os.path.expanduser(path)
        if path == '' or os.path.exists(path):
            self._path = path
            self.path_edit.setText(path)
            self.up_action.setEnabled(bool(path))

    def go_to(self, path=None):
        """Trigger action to go to specified path."""
        if self.update_path(path if path is not None else self.path_edit.text()):
            index = self._view.model().sourceModel().pathIndex(self.path)
            self._view.open_action(self._view.proxy.mapFromSource(index))

    def go_up(self):
        parent = '' if self._path == self._view.model().sourceModel().ROOT_PATH else os.path.dirname(self._path)
        self.go_to(parent)

    def go_home(self):
        self.go_to('~')

    def update_path(self, path):
        """Update displayed path, but do not trigger action.

        Called when the path changed in the view."""
        self.path = path
        return self.path == os.path.expanduser(path)
