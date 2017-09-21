#!/usr/bin/env python3

from ouf import version

from PyQt5 import QtCore, QtWidgets

import argparse
import gettext
import sys


# TODO: icon factory
#       - from theme
#       - local
#       - add emblem
#       - colorize


def parseargs():
    parser = argparse.ArgumentParser(description=version.description)
    parser.add_argument('path', nargs='?', default='~', help='location to open')
    return parser.parse_args()


def main():
    gettext.install(version.name)

    from ouf.mainwindow import MainWindow

    QtCore.QCoreApplication.setApplicationName(version.name)
    QtCore.QCoreApplication.setApplicationVersion(version.version)
    QtCore.QCoreApplication.setOrganizationDomain(version.domain)
    QtCore.QCoreApplication.setOrganizationName(version.organization)

    app = QtWidgets.QApplication(sys.argv)
    args = parseargs()

    w = MainWindow(args.path)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
