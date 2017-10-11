import pytest
from .test_model import fake_filesystem

from ouf.filemodel.filemodel import FileModel
from ouf.filepane import FilePane


@pytest.fixture(scope="function")
def pane_fixture(qtbot, fake_filesystem):
    model = FileModel()
    pane = FilePane(model, str(fake_filesystem))
    qtbot.addWidget(pane)
    return pane


def test_go_up(pane_fixture):
    pathview = pane_fixture.path_view
    pathview.go_to('/')
    assert pathview.path == '/'

    pathview.go_up()
    assert pathview.path == ''
