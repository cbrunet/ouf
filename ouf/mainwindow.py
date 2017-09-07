
from ouf.filemodel.filemodel import FileModel
from ouf.fileview import FileView
from ouf.pathview import PathView

from PyQt5 import QtCore, QtWidgets

from pathlib import Path

# TODO: switch icons / tree
# TODO: application Icon and name
# TODO: new window


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.model = FileModel()

        self.view = FileView()
        self.view.setModel(self.model)

        self.path_view = PathView()
        self.path_view.setView(self.view)
        self.path_view.setPath(str(Path.home()))  # TODO: use argv

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_view)
        layout.addWidget(self.view)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
