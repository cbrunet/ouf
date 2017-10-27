import os
import subprocess
import sys

from PyQt5 import QtCore, QtWidgets

from ouf.filemodel.proxymodel import FileProxyModel
from ouf.view.filenamedelegate import FileNameDelegate
from ouf import shortcuts

# TODO: modifiers to open in new window
# TODO: switch icons / tree
# TODO: modify icon size


class FileView(QtWidgets.QTreeView):

    current_path_changed = QtCore.pyqtSignal(str)

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.proxy = FileProxyModel()
        self.proxy.setSourceModel(model)

        self._create_actions()

        self.setModel(self.proxy)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setSelectionMode(self.ExtendedSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        # self.setAnimated(True)
        self.setEditTriggers(self.SelectedClicked | self.EditKeyPressed)

        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDragDropMode(self.DragDrop)
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)
        self.setAutoExpandDelay(200)

        self._file_name_delegate = FileNameDelegate(self)
        self.setItemDelegateForColumn(0, self._file_name_delegate)

        self.activated.connect(self.open_action)

    def _create_actions(self):
        self.action_delete = QtWidgets.QAction(_("Suppress Selected Files"), self)
        self.action_delete.setShortcuts(shortcuts.delete)
        self.action_delete.triggered.connect(self.delete_selected_files)
        self.action_delete.setEnabled(False)

        self.action_hidden = QtWidgets.QAction(_("Show Hidden Files"), self)
        self.action_hidden.setShortcuts(shortcuts.hidden_files)
        self.action_hidden.setCheckable(True)
        self.action_hidden.setChecked(self.proxy.show_hidden)
        self.action_hidden.toggled.connect(self.show_hide_hidden_files)

    def selectionChanged(self, selected, deselected):
        super().selectionChanged(selected, deselected)
        self.action_delete.setEnabled(bool(self.selectedIndexes()))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if any(u.toLocalFile() for u in event.mimeData().urls()):
                event.accept()
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        pass

    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)
        if event.keyboardModifiers() & QtCore.Qt.CTRL:
            if event.keyboardModifiers() & QtCore.Qt.SHIFT:
                event.setDropAction(QtCore.Qt.LinkAction)
            else:
                event.setDropAction(QtCore.Qt.CopyAction)
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        # index = self.proxy.mapToSource(pindex)
        self.model().dropMimeData(event.mimeData(), event.dropAction(), index.row(), index.column(), index.parent())

    def open_action(self, index):
        """

        Args:
            index: proxy index

        Returns:

        """
        if index.isValid():
            item = self.proxy.mapToSource(index).internalPointer()
            if item.is_lock:
                # TODO: prevent user
                return

            if item.is_dir:
                self.setRootIndex(self.proxy.index(index.row(), 0, index.parent()))
                #TODO: unselect
                self.current_path_changed.emit(item.path)
                QtCore.QCoreApplication.processEvents()  # Ensure the new path is set before resizing
                self.resizeColumnToContents(0)

            else:
                # TODO: open file / exec process / etc.
                if sys.platform.startswith('linux'):
                    subprocess.run(['xdg-open', item.path])
                else:
                    os.startfile(item.path)  # windows
        else:
            # go to root
            self.setRootIndex(index)
            self.current_path_changed.emit("")

    def delete_selected_files(self):
        selection = self.proxy.mapSelectionToSource(self.selectionModel().selection())
        self.proxy.sourceModel().delete_files(selection.indexes())
        self.proxy.invalidate()

    def show_hide_hidden_files(self, show):
        self.proxy.show_hidden = show
