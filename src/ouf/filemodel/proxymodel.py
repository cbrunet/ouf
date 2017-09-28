
from PyQt5 import QtCore

from ouf.filemodel import SortRole


# TODO: show/hide backups files (end with ~)
# TODO: dir first


class FileProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDynamicSortFilter(True)
        # self.setSortCaseSensitivity(False)
        # self.setSortLocaleAware(True)
        # self.setSortRole(SortRole)
        self._show_hidden = False
        self._show_dirs_only = False

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
        if not self.show_hidden:
            name = index.data()
            if name.startswith("."):
                return False

        if self.show_dirs_only:
            if not index.internalPointer().isDir():
                return False

        return super().filterAcceptsRow(source_row, source_parent)

    def lessThan(self, left, right):
        return left.data(SortRole) < right.data(SortRole)
