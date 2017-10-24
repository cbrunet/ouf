from PyQt5 import QtGui, QtCore, QtWidgets


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

        if emblem:
            pass  # TODO: load emblem and add it to icon

        if color:
            pass  # TODO: colorize icon

        return icon


icon_factory = IconFactory()
