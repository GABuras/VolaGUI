from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSortFilterProxyModel
import DataHandling

class ResultWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Results")
        # self.resize(1275, 350)
        self.CreateTable()
        # self.show()
        self.table_view: QtWidgets.QTableView
        self.filter: QSortFilterProxyModel
    
    def CreateTable(self):

        self.vBox = QtWidgets.QVBoxLayout()
        self.vBox.addStretch(0)
        self.vBox.setSpacing(0)
        self.setLayout(self.vBox)
        self.hBox = QtWidgets.QHBoxLayout()
        self.hBox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if DataHandling.service is not None:
            self.PopulateTable(DataHandling.service)
            # sets up the filter dropdown based on service headers
            self.filter_choice = QtWidgets.QComboBox()
            for headers in self.data[DataHandling.service]["headers"]:
                self.filter_choice.addItem(headers)
            # sets up filter based on the table model
            # created in 'PopulateTable()' 
            self.filter = QSortFilterProxyModel()
            self.filter.setSourceModel(self.model)
            # changes filter choice when something in drop down is selected
            self.filter_choice.activated.connect(self.set_filter)
            self.filter_choice.setFixedWidth(250)

            # Creates a search widget using QLineEdit
            self.searchfield = QtWidgets.QLineEdit()
            self.searchfield.setFixedWidth(250)
            self.searchfield.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.searchfield.setPlaceholderText("Search...")
            self.searchfield.setStyleSheet("font-size: 15px; height: 20px;")

            # Connects the filter and the search bar, filtering as text changes
            self.searchfield.textChanged.connect(self.filter.setFilterFixedString)

             # Established horizontal box for the filter and search widgets
            # aligning it to the left side
            self.hBox.addWidget(self.filter_choice)
            self.hBox.addWidget(self.searchfield)

            # sets up a table view of the model
            self.table_view = QtWidgets.QTableView()
            self.table_view.setModel(self.filter)
            self.table_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

            # dynamically stretches the columns to make them fit the widget
            for c in range(self.data[DataHandling.service]["columns"]):
                self.table_view.horizontalHeader().setSectionResizeMode(c, 
                    QtWidgets.QHeaderView.ResizeMode.Stretch)
            #self.table_view.setMaximumHeight(175)
            self.vBox.addLayout(self.hBox)
            self.vBox.addWidget(self.table_view)
            

    def PopulateTable(self, service):
        # grabs the command data dictionary
        self.data = DataHandling.command_data
        # pulls command specific column count
        columns = self.data[service]["columns"]
        #dynamically calculates the length of data in the file
        rows = self.data[f"service"]["rows"](f"{service}.txt")
        # established model of data
        self.model = QtGui.QStandardItemModel(rows, columns)
        # sets data model headers
        self.model.setHorizontalHeaderLabels(self.data[service]["headers"])

        # loops through the file to populate the model
        with open(f"./data/{service}.txt", "r") as file:
            for r in range(rows):
                entry = file.readline()
                column_entries = entry.split(",")
                for c in range(columns):
                    item = QtGui.QStandardItem(str(column_entries[c]))
                    self.model.setItem(r, c, item)
    
    # used to set the filter when changed
    def set_filter(self):
        self.filter.setFilterKeyColumn(self.filter_choice.currentIndex())
