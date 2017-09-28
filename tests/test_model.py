from ouf.filemodel.filemodel import FileModel
from PyQt5 import QtCore


def test_create_new_directory(tmpdir):
    model = FileModel()

    for i, dirname in enumerate(('New Folder', 'New Folder (1)', 'New Folder (2)')):
        index = model.create_new_directory(tmpdir)
        assert tmpdir.join(dirname).isdir()  # The directory effectively was created on the filesystem
        assert index.isValid()  # The returned index is a valid index
        assert index.data(QtCore.Qt.UserRole) == tmpdir.join(dirname)  # The path returned by the index is ok
        assert model.rowCount(index.parent()) == i + 1  # The number of directory in the parent directory is as expected
        assert index.row() == i  # The row number is the ith element we created
