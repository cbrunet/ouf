
import os.path
from PyQt5 import QtCore

from ouf.filemodel import SortRole


# TODO: show/hide backups files (end with ~)
# TODO: dir first


class FileProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_path = ""

        self.setDynamicSortFilter(True)
        # self.setSortCaseSensitivity(False)
        # self.setSortLocaleAware(True)
        # self.setSortRole(SortRole)
        self._show_hidden = False
        self._show_dirs_only = False

    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, path):
        self.invalidate()
        self._current_path = path

    @property
    def show_hidden(self):
        return self._show_hidden

    @show_hidden.setter
    def show_hidden(self, show):
        self._show_hidden = show
        self.invalidate()  # Why doesn't invalidateFilter work?

    @property
    def show_dirs_only(self):
        return self._show_dirs_only

    @show_dirs_only.setter
    def show_dirs_only(self, show):
        self._show_dirs_only = show
        self.invalidate()  # Why doesn't invalidateFilter work?

    def filterAcceptsRow(self, source_row, source_parent):
        """

        Args:
            source_row:
            source_parent:

        Returns:

        """
        index = self.sourceModel().index(source_row, 0, source_parent)

        if index.isValid():
            item = index.internalPointer()

            if self.current_path.startswith(item.path):
                # Allow to navigate in hidden folder even if not visible
                return True

            if not self.show_hidden:
                return not item.is_hidden

            if self.show_dirs_only:
                if not item.is_dir:
                    return False

        return super().filterAcceptsRow(source_row, source_parent)

    def lessThan(self, left, right):
        if left.isValid() and right.isValid():
            return left.data(SortRole) < right.data(SortRole)
        return False
