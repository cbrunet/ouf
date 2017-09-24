
from PyQt5 import QtWidgets

from ouf.pathview import PathView
from ouf.view.fileview import FileView


class FilePane(QtWidgets.QWidget):

    def __init__(self, model, path, parent=None):
        super().__init__(parent)

        self.view = FileView(model)
        self.path_view = PathView(path, self.view)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_view)
        layout.addWidget(self.view)

        self.setLayout(layout)

    @property
    def current_directory(self):
        return self.path_view.path
