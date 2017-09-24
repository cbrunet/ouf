from PyQt5 import QtWidgets


class FileNameDelegate(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        self._editor = QtWidgets.QLineEdit(parent)

        return self._editor

    def setEditorData(self, editor, index):
        editor.setText(index.data())

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
