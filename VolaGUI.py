import sys
import typing

from PyQt6 import QtGui
import ResultTable
import ButtonWidget
import QueueWidget
import CommandDescription
import DataHandling
# from CommandDropdown_Test import CommandDropdown
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

commands = {"DLLs": ["dlldump", "dlllist"],
                "Modules": ["moddump", "modules", "modscan"],
                "Processes": ["pslist", "psscan", "pstree"],
                "Registry": ["hivedump", "hivelist", "hivescan"]}

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("VolaGUI")
        self.set_window()

    def set_window(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(1)

        self.Results = ResultTable.ResultWidget()
        self.Description = CommandDescription.Window()

        """Tree Selection Commands"""
        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Commands"])
        tree.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        commands = []
        for key, values in DataHandling.command_list.items():
            command = QTreeWidgetItem([key])
            for value in values:
                command_item = QTreeWidgetItem([value])
                command.addChild(command_item)
            commands.append(command)
        tree.insertTopLevelItems(0, commands)
        tree.itemClicked.connect(self.update_windows)

        self.CommandMenu = tree
        """Tree Selection Commands"""

        #Select and Show Command Area 
        self.layout.addWidget(self.CommandMenu, 0, 0,2,1)

        self.layout.addWidget(Color("red"), 2, 0, 1, 1)

        # Results Area
        self.layout.addWidget(self.Results, 3,0, -1, -1, 
                         alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)

        #Command Description Area
        self.layout.addWidget(self.Description, 0, 1,2,1)

        # Command Building Area
        self.layout.addWidget(Color('purple'), 2, 1,1,1)

        #Command Queue Area
        self.layout.addWidget(QueueWidget.Window(), 0, 2,2,1)

        #Queue Command Button
        #layout.addWidget(Color('yellow'), 1, 2,1,1)

        #Queue Command Button & Execute Command Button
        #layout.addWidget(Color('black'), 2, 2,1,1)
        self.layout.addWidget(ButtonWidget.Window(), 2, 2,1,1)
        
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    @pyqtSlot(QTreeWidgetItem, int)
    def update_windows(self, it, col):
        command = it.text(col)
        if command in ["pslist", "psscan"]:
            if command is DataHandling.service:
                return
            DataHandling.service = command
            self.Description.hide()
            self.Description = CommandDescription.Window()
            self.layout.addWidget(self.Description, 0, 1,2,1)
    
app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
app.exec()