from ouf.mainwindow import MainWindow

from PyQt5 import QtWidgets

import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
