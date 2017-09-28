import pytest

from ouf.filemodel.filemodel import FileModel
from PyQt5 import QtCore


@pytest.fixture(scope='function')
def fake_filesystem(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("root")
    dir_a = tmpdir.mkdir("dir A")
    dir_b = tmpdir.mkdir("dir B")
    open(dir_a.join("file a"), 'a')
    open(dir_a.join("file b"), 'a')
    open(dir_a.join("file c"), 'a')
    open(dir_b.join("file d"), 'a')
    return tmpdir


def test_create_new_directory(tmpdir):
    model = FileModel()

    for i, dirname in enumerate(('New Folder', 'New Folder (1)', 'New Folder (2)')):
        index = model.create_new_directory(tmpdir)
        assert tmpdir.join(dirname).isdir()  # The directory effectively was created on the filesystem
        assert index.isValid()  # The returned index is a valid index
        assert index.data(QtCore.Qt.UserRole) == tmpdir.join(dirname)  # The path returned by the index is ok
        assert model.rowCount(index.parent()) == i + 1  # The number of directory in the parent directory is as expected
        assert index.row() == i  # The row number is the ith element we created


def test_move_file(fake_filesystem):
    model = FileModel()

    dir_a_index = model.pathIndex(fake_filesystem.join("dir A"))
    dir_b_index = model.pathIndex(fake_filesystem.join("dir B"))

    model._move_file(fake_filesystem.join("dir A", "file a"), dir_b_index)

    # Ensure the file moved on the filesystem
    assert not fake_filesystem.join("dir A", "file a").exists()
    assert fake_filesystem.join("dir B", "file a").exists()

    # Ensure the model was updated accordingly
    assert model.rowCount(dir_a_index) == 2
    assert model.rowCount(dir_b_index) == 2


def test_delete_files(fake_filesystem):
    model = FileModel()

    dir_a_index = model.pathIndex(fake_filesystem.join("dir A"))
    dir_b_index = model.pathIndex(fake_filesystem.join("dir B"))
    file_a = model.pathIndex(fake_filesystem.join("dir A", "file a"))
    file_b = model.pathIndex(fake_filesystem.join("dir A", "file b"))

    # Delete one file
    model.delete_files([file_a])
    assert not fake_filesystem.join("dir A", "file a").exists()
    assert model.rowCount(dir_a_index) == 2

    # Delete one dir and one file
    model.delete_files([dir_b_index, file_b])
    assert not fake_filesystem.join("dir B").exists()
    assert model.rowCount(dir_a_index) == 1
