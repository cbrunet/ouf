#!/usr/bin/env python3

from ouf.mainwindow import MainWindow
from ouf import version

from PyQt5 import QtCore, QtWidgets

import argparse
import sys


def parseargs():
    parser = argparse.ArgumentParser(description=version.description)
    parser.add_argument('path', nargs='?', default='~', help='location to open')
    return parser.parse_args()


def main():

    QtCore.QCoreApplication.setApplicationName("ouf")
    QtCore.QCoreApplication.setApplicationVersion(version.version)
    QtCore.QCoreApplication.setOrganizationDomain("cbrunet.net")
    QtCore.QCoreApplication.setOrganizationName("cbrunet")

    app = QtWidgets.QApplication(sys.argv)
    args = parseargs()

    w = MainWindow(args.path)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
