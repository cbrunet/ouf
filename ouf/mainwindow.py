
from ouf.filemodel.filemodel import FileModel
from ouf.filepane import FilePane

from PyQt5 import QtCore, QtGui, QtWidgets

import subprocess
import sys

# TODO: save/restore windows state


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.tr("Universal File Organiser"))
        self.setWindowIcon(QtGui.QIcon.fromTheme('system-file-manager'))

        self.model = FileModel()

        self.pane = FilePane(self.model, path, self)

        self._create_actions()
        self._create_menus()

        self.setCentralWidget(self.pane)

    def _create_actions(self):
        self.action_new = QtWidgets.QAction(self.tr("New Window"), self)
        self.action_new.setShortcuts(QtGui.QKeySequence(self.tr("Ctrl+N")))
        self.action_new.triggered.connect(self.on_action_new)

    def _create_menus(self):
        app_menu = self.menuBar().addMenu(self.tr("Ufo"))
        app_menu.addAction(self.action_new)
        # new tab
        # close / quit

        ## File
        # new directory
        # new file
        # new...
        # cut / copy / paste
        # delete
        # select all / none

        go_menu = self.menuBar().addMenu(self.tr("Go"))
        # back
        # forward
        go_menu.addAction(self.pane.path_view.up_action)
        go_menu.addAction(self.pane.path_view.home_action)

        ## View
        # Show/hide hidden files
        # Directory tree
        # File preview
        # Split / unsplit

        ## Help
        # About
        # Help
        # Whats this

    def on_action_new(self):
        args = [sys.argv[0], self.pane.current_directory()]
        subprocess.Popen(args)
