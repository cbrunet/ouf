from functools import lru_cache
from PyQt5 import QtGui, QtCore, QtWidgets


@lru_cache()
def add_emblem(icon, emblem, position):

    px = (position & 1) / 2
    py = (position & 2) / 4

    new_icon = QtGui.QIcon()
    for mode in QtGui.QIcon.Normal, QtGui.QIcon.Disabled, QtGui.QIcon.Active, QtGui.QIcon.Selected:
        for state in QtGui.QIcon.On, QtGui.QIcon.Off:
            for size in icon.availableSizes(mode, state):
                icon_pixmap = icon.pixmap(size, mode, state)
                emblem_pixmap = emblem.pixmap(size.width() / 2, size.height() / 2, mode, state)
                painter = QtGui.QPainter(icon_pixmap)
                painter.drawPixmap(size.width() * px, size.height() * py, emblem_pixmap)
                painter.end()
                new_icon.addPixmap(icon_pixmap, mode, state)
    return new_icon


class IconFactory(object):

    def __init__(self):
        self.provider = QtWidgets.QFileIconProvider()

    def __call__(self, fsitem, emblem=False, color=False):
        icon = None
        mimetype = None

        # TODO: handle info from desktop files first

        if fsitem.is_dir:
            if fsitem.is_home:
                mimetype = "user-home"

            elif fsitem.is_root:
                icon = self.provider.icon(self.provider.Computer)
                mimetype = "computer"

            # TODO: detect mount points

            else:
                icon = self.provider.icon(self.provider.Folder)
                mimetype = "folder"

        if not icon:
            if not mimetype:
                mimetype = fsitem.mimetype.replace("/", "-")

            if not mimetype:
                # TODO: detect executable files

                icon = self.provider.icon(self.provider.File)

        if not icon:
            if QtGui.QIcon.hasThemeIcon(mimetype):
                icon = QtGui.QIcon.fromTheme(mimetype)

            else:
                fileinfo = QtCore.QFileInfo(fsitem.path)
                icon = self.provider.icon(fileinfo)

        # TODO: set emblem for symbolic links

        if fsitem.is_lock:
            icon = add_emblem(icon, QtGui.QIcon.fromTheme("emblem-unreadable"), 3)
        elif fsitem.is_link:
            icon = add_emblem(icon, QtGui.QIcon.fromTheme("emblem-symbolic-link"), 3)


        if color:
            pass  # TODO: colorize icon

        return icon


icon_factory = IconFactory()
