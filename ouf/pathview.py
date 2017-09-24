from ouf import shortcuts

from PyQt5 import QtCore, QtGui, QtWidgets

import os.path


# TODO: location icon
# TODO: allow to go to hidden path


class PathView(QtWidgets.QWidget):

    def __init__(self, path, view, parent=None):
        super().__init__(parent)

        self._create_actions()
        self._create_layout()

        self._view = view
        view.current_path_changed.connect(self.update_path)

        self._paths = []
        self._path_index = -1
        self.go_to(path)

    def _create_actions(self):
        self.up_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-up'), _("Parent Directory"), self)
        self.up_action.setEnabled(False)
        self.up_action.setShortcuts(shortcuts.go_up)
        self.up_action.triggered.connect(self.go_up)

        self.back_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-previous'), _("Previous"), self)
        self.back_action.setEnabled(False)
        self.back_action.setShortcuts(shortcuts.go_back)
        self.back_action.triggered.connect(self.go_back)

        self.forth_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-next'), _("Previous"), self)
        self.forth_action.setEnabled(False)
        self.forth_action.setShortcuts(shortcuts.go_forth)
        self.forth_action.triggered.connect(self.go_forth)

        self.home_action = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-home'), _("Home"), self)
        self.home_action.setShortcuts(shortcuts.go_home)
        self.home_action.triggered.connect(self.go_home)

    def _create_layout(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.up_button = QtWidgets.QToolButton()
        self.up_button.setDefaultAction(self.up_action)

        self.back_button = QtWidgets.QToolButton()
        self.back_button.setDefaultAction(self.back_action)

        self.forth_button = QtWidgets.QToolButton()
        self.forth_button.setDefaultAction(self.forth_action)

        self.home_button = QtWidgets.QToolButton()
        self.home_button.setDefaultAction(self.home_action)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.editingFinished.connect(self.go_to)
        # TODO: add validator to normalize path, resolve home, etc.

        layout.addWidget(self.back_button)
        layout.addWidget(self.up_button)
        layout.addWidget(self.forth_button)
        layout.addWidget(self.home_button)
        layout.addWidget(self.path_edit)
        self.setLayout(layout)

    def _update_actions(self):
        self.up_action.setEnabled(bool(self.path))
        self.back_action.setEnabled(self._path_index > 0)
        self.forth_action.setEnabled(self._path_index < len(self._paths) - 1)

    @property
    def path(self):
        return self._paths[self._path_index] if self._path_index >= 0 else None

    @path.setter
    def path(self, path):
        path = os.path.expanduser(path)
        if path == '' or (path != self.path and os.path.exists(path)):
            self._path_index += 1
            self._paths = self._paths[:self._path_index]
            self._paths.append(path)
            self.path_edit.setText(path)
            self._update_actions()

    def go_back(self):
        if self._path_index > 0:
            self._path_index -= 1
            self.path_edit.setText(self.path)
            self.go_to(self.path)
            self._update_actions()

    def go_forth(self):
        if self._path_index + 1 < len(self._paths):
            self._path_index += 1
            self.path_edit.setText(self.path)
            self.go_to(self.path)
            self._update_actions()

    def go_to(self, path=None):
        """Trigger action to go to specified path."""
        if self.update_path(path if path is not None else self.path_edit.text()):
            index = self._view.model().sourceModel().pathIndex(self.path)
            self._view.open_action(self._view.proxy.mapFromSource(index))

    def go_up(self):
        parent = '' if self.path == self._view.model().sourceModel().ROOT_PATH else os.path.dirname(self.path)
        self.go_to(parent)

    def go_home(self):
        self.go_to('~')

    def update_path(self, path):
        """Update displayed path, but do not trigger action.

        Called when the path changed in the view."""
        path = path.rstrip(os.sep)
        self.path = path
        return self.path == os.path.expanduser(path)
