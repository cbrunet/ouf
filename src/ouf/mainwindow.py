import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from ouf.filemodel.filemodel import FileModel
from ouf.filepane import FilePane

from ouf import shortcuts


# TODO: save/restore windows state


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, path, parent=None):
        super().__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(_("Universal File Organiser"))
        self.setWindowIcon(QtGui.QIcon.fromTheme('system-file-manager'))

        self.model = FileModel()
        self.pane = FilePane(self.model, path, self)

        self._create_actions()
        self._create_menus()

        self.setCentralWidget(self.pane)

    def _create_actions(self):
        self.action_new = QtWidgets.QAction(_("New Window"), self)
        self.action_new.setShortcuts(shortcuts.new_window)
        self.action_new.triggered.connect(self.on_action_new)

        self.action_close = QtWidgets.QAction(_("Close Window"), self)
        self.action_close.setShortcuts(shortcuts.close_window)
        self.action_close.triggered.connect(self.close)

        self.action_new_folder = QtWidgets.QAction(_("New Folder"), self)
        self.action_new_folder.setShortcuts(shortcuts.new_folder)
        self.action_new_folder.triggered.connect(self.create_new_directory)

    def _create_menus(self):
        app_menu = self.menuBar().addMenu(_("Ufo"))
        app_menu.addAction(self.action_new)
        # new tab
        app_menu.addAction(self.action_close)

        file_menu = self.menuBar().addMenu(_("File"))
        file_menu.addAction(self.action_new_folder)
        # new file
        # new...
        # cut / copy / paste
        file_menu.addAction(self.pane.view.action_delete)
        # select all / none

        go_menu = self.menuBar().addMenu(_("Go"))
        # TODO: open
        go_menu.addAction(self.pane.path_view.back_action)
        go_menu.addAction(self.pane.path_view.forth_action)
        go_menu.addAction(self.pane.path_view.up_action)
        go_menu.addAction(self.pane.path_view.home_action)

        ## View
        view_menu = self.menuBar().addMenu(_("View"))
        view_menu.addAction(self.pane.view.action_hidden)
        # Directory tree
        # File preview
        # Split / unsplit

        ## Help
        # About
        # Help
        # Whats this

    def on_action_new(self):
        args = [sys.argv[0], self.pane.current_directory]
        subprocess.Popen(args)

    def create_new_directory(self):
        index = self.model.create_new_directory(self.pane.current_directory)
        self.pane.view.proxy.invalidate()
        pindex = self.pane.view.proxy.mapFromSource(index)
        self.pane.view.setCurrentIndex(pindex)  # TODO: why doesn't it work?
