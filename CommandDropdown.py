from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PyQt6.QtCore import pyqtSlot


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        
        tree = QTreeWidget()  # add parent here
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Commands"])

        # command list (TODO: add 'list all')
        data = {"DLLs": ["dlldump", "dlllist"],
                "Modules": ["moddump", "modules", "modscan"],
                "Processes": ["pslist", "psscan", "pstree"],
                "Registry": ["hivedump", "hivelist", "hivescan"]}

        # add data to the tree
        commands = []
        for key, values in data.items():
            command = QTreeWidgetItem([key])
            for value in values:
                ext = value.split(".")[-1]
                child = QTreeWidgetItem([value, ext])
                command.addChild(child)
            commands.append(command)

        tree.insertTopLevelItems(0, commands)
        tree.itemClicked.connect(self.onItemClick)  # make menu items clickable

    @pyqtSlot(QTreeWidgetItem, int)
    def onItemClick(self, it, col):
        match it.text(col):
            case "pslist":
                print('psslist case')
            case "psscan":
                print('psscan case')
            case _:
                print(f"The button {it.text(col)} has been pressed.")
