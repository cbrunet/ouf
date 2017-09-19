

from PyQt5 import QtCore


class FileProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDynamicSortFilter(True)
        self.setSortCaseSensitivity(False)
        self.setSortLocaleAware(True)
        self._show_hidden = False

    @property
    def show_hidden(self):
        return self._show_hidden

    @show_hidden.setter
    def show_hidden(self, show):
        self._show_hidden = show
        self.invalidate()  # Why doesn't invalidateFilter work?

    def filterAcceptsRow(self, source_row, source_parent):
        """

        Args:
            source_row:
            source_parent:

        Returns:

        """
        if not self.show_hidden:
            index = self.sourceModel().index(source_row, 0, source_parent)
            name = index.data()
            if name.startswith("."):
                return False

        return super().filterAcceptsRow(source_row, source_parent)
