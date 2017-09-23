
from PyQt5 import QtGui


# Ufo
new_window = QtGui.QKeySequence(_("Ctrl+N"))

# File
new_folder = QtGui.QKeySequence(_("Ctrl+Shift+N"))
delete = [QtGui.QKeySequence(_("Delete")), QtGui.QKeySequence(_("Backspace"))]

# Go
go_up = QtGui.QKeySequence(_("Ctrl+Up"))
go_home = [QtGui.QKeySequence(_("Ctrl+Home")), QtGui.QKeySequence(_("Alt+Home"))]

# View
hidden_files = QtGui.QKeySequence(_("Ctrl+H"))