from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import sys;
import DataHandling

class Window(QtWidgets.QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setWindowTitle("Results")
        self.resize(1250, 350)
        self.CreateTable()
        self.show()
    
    def CreateTable(self):
        self.table = QtWidgets.QTableWidget()
        # self.table.setRowCount(5)
        # self.table.setColumnCount(3)
        self.PopulateTable(self.service)
        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.addWidget(self.table)
        self.setLayout(self.vBox)
    def PopulateTable(self, service):
        # grabs the command data dictionary
        data = DataHandling.command_data
        # pulls command specific column count
        columns = data[service]["columns"]
        #dynamically calculates the length of data in the file
        rows = data["rows"](f"{service}.txt")
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        self.table.setHorizontalHeaderLabels(data[service]["headers"])

        with open(f"./data/{service}.txt", "r") as file:
            for r in range(rows):
                entry = file.readline()
                column_entries = entry.split(",")
                for c in range(columns):
                    self.table.setItem(r, c, QtWidgets.QTableWidgetItem(str(column_entries[c])))

choice = input("Please type pslist or psscan to get results: ")
app = QtWidgets.QApplication(sys.argv)
window = Window(choice)
sys.exit(app.exec())