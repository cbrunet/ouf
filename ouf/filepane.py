
from ouf.fileview import FileView
from ouf.pathview import PathView

from PyQt5 import QtWidgets

# TODO: use proxy model

class FilePane(QtWidgets.QWidget):

    def __init__(self, model, path, parent=None):
        super().__init__(parent)

        self.view = FileView()
        self.view.setModel(model)

        self.path_view = PathView()
        self.path_view.setView(self.view)
        self.path_view.setPath(path)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_view)
        layout.addWidget(self.view)

        self.setLayout(layout)

    def current_directory(self):
        return self.path_view.path_edit.text()