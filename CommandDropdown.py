import sys
from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import pyqtSlot


# command list (TODO: add 'list all')
data = {"DLLs": ["dlldump", "dlllist"],
        "Modules": ["moddump", "modules", "modscan"],
        "Processes": ["pslist", "psscan", "pstree"],
        "Registry": ["hivedump", "hivelist", "hivescan"]}

app = QApplication([])

tree = QTreeWidget()  # add parent here
tree.setColumnCount(1)
tree.setHeaderLabels(["Commands"])

# onClick function for the commands
@pyqtSlot(QTreeWidgetItem, int)
def onItemClick(it, col):
    match it.text(col):
        case "pslist":
            print('psslist case')
        case "psscan":
            print('psscan case')
        case _:
            print(f"The button {it.text(col)} has been pressed.")

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
tree.itemClicked.connect(onItemClick)  # make menu items clickable

tree.show()
sys.exit(app.exec())
