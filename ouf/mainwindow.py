
from ouf.filemodel.filemodel import FileModel
from ouf.filepane import FilePane

from PyQt5 import QtCore, QtGui, QtWidgets

import subprocess
import sys

# TODO: new window
# TODO: save/restore windows state


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr("Universal File Organiser"))
        self.setWindowIcon(QtGui.QIcon.fromTheme('system-file-manager'))

        self.model = FileModel()

        self.pane = FilePane(self.model, path, self)

        self._createActions()
        self._createMenus()

        self.setCentralWidget(self.pane)

    def _createActions(self):
        self.action_new = QtWidgets.QAction(self.tr("New Window"), self)
        self.action_new.setShortcuts(QtGui.QKeySequence(self.tr("Ctrl+N")))
        self.action_new.triggered.connect(self.onActionNew)

    def _createMenus(self):
        app_menu = self.menuBar().addMenu(self.tr("Ufo"))
        app_menu.addAction(self.action_new)

        go_menu = self.menuBar().addMenu(self.tr("Go"))
        go_menu.addAction(self.pane.path_view.up_action)

    def onActionNew(self):
        args = [sys.argv[0], self.pane.current_directory()]
        subprocess.Popen(args)
