
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


# Ufo
new_window = QtGui.QKeySequence(_("Ctrl+N"))
close_window = [QtGui.QKeySequence(_("Ctrl+W")), QtGui.QKeySequence(_("Ctrl+Q"))]

# File
new_folder = QtGui.QKeySequence(_("Ctrl+Shift+N"))
delete = [QtGui.QKeySequence(_("Delete")), QtGui.QKeySequence(_("Backspace"))]

# Go
go_in = [QtGui.QKeySequence(_("Ctrl+Down")), QtGui.QKeySequence(_("Alt+Down"))]
go_up = [QtGui.QKeySequence(_("Ctrl+Up")), QtGui.QKeySequence(_("Alt+Up"))]
go_back = [QtGui.QKeySequence(_("Alt+Left")), QtGui.QKeySequence(Qt.Key_Back)]
go_forth = [QtGui.QKeySequence(_("Alt+Right")), QtGui.QKeySequence(Qt.Key_Forward)]
go_home = [QtGui.QKeySequence(_("Ctrl+Home")), QtGui.QKeySequence(_("Alt+Home")), QtGui.QKeySequence(Qt.Key_HomePage)]

# View
hidden_files = QtGui.QKeySequence(_("Ctrl+H"))