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


def test_model(qtmodeltester):
    model = FileModel()
    qtmodeltester.check(model)


def test_create_new_directory(tmpdir):
    model = FileModel()

    for i, dirname in enumerate(('New Folder', 'New Folder (1)', 'New Folder (2)')):
        index = model.create_new_directory(tmpdir)
        assert tmpdir.join(dirname).isdir()  # The directory effectively was created on the filesystem
        assert index.isValid()  # The returned index is a valid index
        assert index.data(QtCore.Qt.UserRole) == tmpdir.join(dirname)  # The path returned by the index is ok
        assert model.rowCount(index.parent()) == i + 1  # The number of directory in the parent directory is as expected
        assert index.row() == i  # The row number is the ith element we created


def test_rename_file(fake_filesystem):
    model = FileModel()

    file_a_index = model.pathIndex(fake_filesystem.join("dir A", "file a"))
    model.setData(file_a_index, "file e")

    assert model.rowCount(file_a_index.parent()) == 3
    assert not fake_filesystem.join("dir A", "file a").exists()
    assert fake_filesystem.join("dir A", "file e").exists()
    assert model.data(file_a_index, QtCore.Qt.UserRole) == fake_filesystem.join("dir A", "file e")


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


def test_copy_file(fake_filesystem):
    model = FileModel()

    dir_b_index = model.pathIndex(fake_filesystem.join("dir B"))

    # Copy file
    model._copy_file(fake_filesystem.join("dir A", "file a"), dir_b_index)
    assert fake_filesystem.join("dir A", "file a").exists()
    assert fake_filesystem.join("dir B", "file a").exists()


def test_copy_directory(fake_filesystem):
    model = FileModel()

    dir_a_index = model.pathIndex(fake_filesystem.join("dir A"))

    # Copy directory
    model._copy_file(fake_filesystem.join("dir B"), dir_a_index)
    assert fake_filesystem.join("dir A", "dir B", "file d").exists()
    assert fake_filesystem.join("dir B", "file d").exists()


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
