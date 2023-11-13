import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSlot
import DataHandling

commands = {"DLLs": ["dlldump", "dlllist"],
                "Modules": ["moddump", "modules", "modscan"],
                "Processes": ["pslist", "psscan", "pstree"],
                "Registry": ["hivedump", "hivelist", "hivescan"]}

class CommandDropdown(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        tree = QtWidgets.QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Commands"])
        tree.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

        # Command Dropdown List
        data = {
            "DLLs": ["dlldump", "dlllist"],
            "Modules": ["moddump", "modules", "modscan"],
            "Processes": ["pslist", "psscan", "pstree"],
            "Registry": ["hivedump", "hivelist", "hivescan"]
        }

        commands = []
        for key, values in data.items():
            command = QtWidgets.QTreeWidgetItem([key])
            for value in values:
                command_item = QtWidgets.QTreeWidgetItem([value])
                command.addChild(command_item)
            commands.append(command)
        tree.insertTopLevelItems(0, commands)
        tree.itemClicked.connect(self.onItemClick)
        self.vBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vBox)
        self.vBox.addWidget(tree)
        self.vBox.setStretch(1, 0)

    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClick(self, it, col):
        command = it.text(col)
        if command in ["pslist", "psscan"]:
            if command is DataHandling.service:
                return
            DataHandling.service = command
            DataHandling.service_changed = True