from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSortFilterProxyModel
import sys;
import DataHandling

class Window(QtWidgets.QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setWindowTitle("Results")
        self.resize(1275, 350)
        self.CreateTable()
        self.show()
        self.filter: QSortFilterProxyModel
    
    def CreateTable(self):
        self.PopulateTable(self.service)
        self.vBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vBox)

        searchfield = QtWidgets.QLineEdit()

        self.filter_choice = QtWidgets.QComboBox()
        for headers in self.data[self.service]["headers"]:
            self.filter_choice.addItem(headers)

        self.filter = QSortFilterProxyModel()
        self.filter.setSourceModel(self.model)

        self.filter_choice.activated.connect(self.set_filter)

        searchfield.setStyleSheet("font-size: 20px; height: 35px;")
        searchfield.textChanged.connect(self.filter.setFilterFixedString)

        self.vBox.addWidget(self.filter_choice)
        self.vBox.addWidget(searchfield)
        table_view = QtWidgets.QTableView()
        table_view.setModel(self.filter)
        self.vBox.addWidget(table_view)

    def PopulateTable(self, service):
        # grabs the command data dictionary
        self.data = DataHandling.command_data
        # pulls command specific column count
        columns = self.data[service]["columns"]
        #dynamically calculates the length of data in the file
        rows = self.data["rows"](f"{service}.txt")
        self.model = QtGui.QStandardItemModel(rows, columns)
        self.model.setHorizontalHeaderLabels(self.data[service]["headers"])

        with open(f"./data/{service}.txt", "r") as file:
            for r in range(rows):
                entry = file.readline()
                column_entries = entry.split(",")
                for c in range(columns):
                    item = QtGui.QStandardItem(str(column_entries[c]))
                    self.model.setItem(r, c, item)
    
    def set_filter(self):
        self.filter.setFilterKeyColumn(self.filter_choice.currentIndex())

choice = input("Please type pslist or psscan to get results: ")
app = QtWidgets.QApplication(sys.argv)
window = Window(choice)
sys.exit(app.exec())