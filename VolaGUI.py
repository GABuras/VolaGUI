import sys
import typing

from PyQt6 import QtGui, QtWidgets
# import ResultTable
# import QueueWidget
# import CommandDescription
import DataHandling
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QRect, QSortFilterProxyModel
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


global window

# _______________________________________________________________________________
# CommandDecription.py

class CommandDescFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.generate_description()
        self.setStyleSheet("QFrame { border: 1px solid black; border-style: outset;}")
        self.setFixedSize(1100, 450)

    def generate_description(self):
        service = DataHandling.service
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        header = QLabel(f"Command Description: {service}")
        font = header.font()
        font.setPointSize(20)
        header.setFont(font)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setScaledContents(False)
        header.setFixedHeight(35)
        header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.data = DataHandling.command_data
        headerlayout = QHBoxLayout()
        headerlayout.addWidget(header)
        description = QLabel(None)
        CommandInfo = QLabel(None)

        self.layout.addLayout(headerlayout)
        if service is not None:
            description = QLabel(self.data[service]["description"])
            font = description.font()
            font.setPointSize(15)
            description.setFont(font)
            description.setAlignment(Qt.AlignmentFlag.AlignLeft)
            description.setScaledContents(False)
            description.setWordWrap(True)

            CommandInfo = QLabel(self.data[service]["info"])
            font = CommandInfo.font()
            font.setPointSize(15)
            CommandInfo.setFont(font)
            CommandInfo.setAlignment(Qt.AlignmentFlag.AlignLeft)
            CommandInfo.setScaledContents(False)
            CommandInfo.setWordWrap(True)

        # description.setStyleSheet("border: 1px solid black;")
        # CommandInfo.setStyleSheet("border: 1px solid black;")

        self.layout.addWidget(description)
        self.layout.addWidget(CommandInfo)


# _______________________________________________________________________________
# CommandDropdown.py

class CommandDropdownFrame(QFrame):
    commandSelected = pyqtSignal(str)  # Custom signal to notify when a command is selected

    def __init__(self):
        super().__init__()
        self.setup_dropdown()
        self.setStyleSheet("QFrame { border: 1px solid black; }")  # Customize the border style if needed
        self.setFixedSize(200, 300)  # Set your desired width and height

    def setup_dropdown(self):
        tree = QtWidgets.QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Commands"])
        tree.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

        commands = []
        for key, values in DataHandling.command_list.items():
            command = QtWidgets.QTreeWidgetItem([key])
            for value in values:
                command_item = QtWidgets.QTreeWidgetItem([value])
                command.addChild(command_item)
            commands.append(command)
        tree.insertTopLevelItems(0, commands)
        tree.itemClicked.connect(self.on_item_click)

        v_box = QtWidgets.QVBoxLayout(self)
        v_box.addWidget(tree)
        v_box.setStretch(1, 0)

    @pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_item_click(self, it, col):
        command = it.text(col)
        self.commandSelected.emit(command)


# _______________________________________________________________________________
# CommandLineBuilder.py

class CLBuilderWidget(QWidget):
    def __init__(self, pid):
        super().__init__()

        self.label = QLabel('text goes here')

        # button for testing
        self.button = QPushButton('press me!')
        self.button.clicked.connect(self.psscan_cl)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    """psscan command line builder function"""
    def psscan_cl(self):
        self.label.setText('./vol.py -f mem.img windows.psscan')

    """pslist command line builder function"""
    def pslist_cl(self, pid=None):
        self.label.setText('python3 vol.py -f mem.img windows.pslist')
        if pid is not None:
            self.label.setText(f'python3 vol.py -f mem.img windows.pslist -p {pid}')


# _______________________________________________________________________________
# QueueWidget.py

class QueueWindow(QFrame):

    def __init__(self,parent=None):
        super().__init__(parent)

        header = QLabel("Queue:")
        self.setStyleSheet("QFrame { border: 1px solid black; }")
        self.setFixedSize(300, 450)
        font = header.font()
        font.setPointSize(20)
        header.setFont(font)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setScaledContents(False)
        # header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        header.setFixedHeight(35)

        # command = QLineEdit()
        # command.setPlaceholderText("<Command>")
        # command.setReadOnly(True)
        # command.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        headerlayout = QHBoxLayout()
        headerlayout.addWidget(header)
        # headerlayout.addWidget(command)
        
        global queue # Necessary to allow the button click handling code in ButtonWidget.py to update queue contents. Fix if you know how to
        queue = QListWidget()
        # Placeholder text would be ideal, but seems a little complicated, so maybe do later
        
        # queue.addItems(["One", "Two", "Three"])

        # queue.currentItemChanged.connect(self.index_changed)
        # queue.currentTextChanged.connect(self.text_changed)
        queue.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)


        layout = QVBoxLayout()
    
        layout.addLayout(headerlayout)

        layout.addWidget(queue)
        layout.setSpacing(0)


        self.setLayout(layout)

    # def index_changed(self, i): # Not an index, i is a QListWidgetItem
    #     print(i.text())

    # def text_changed(self, s): # s is a str
    #     print(s)

def add_to_queue(command: str): # command is the name of the command
    queue.addItem(command)
    print("Added " + command + " to queue")

def execute_queue(): 
    # for command in queue, execute and display results
    queue.clear()
    print("Executed queue")


# _______________________________________________________________________________
# ResultTable.py

class ResultWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.CreateTable()
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
            self.filter_choice = QtWidgets.QComboBox()
            for headers in self.data[DataHandling.service]["headers"]:
                self.filter_choice.addItem(headers)
            self.filter = QSortFilterProxyModel()
            self.filter.setSourceModel(self.model)
            self.filter_choice.activated.connect(self.set_filter)
            self.filter_choice.setFixedWidth(250)

            self.searchfield = QtWidgets.QLineEdit()
            self.searchfield.setFixedWidth(250)
            self.searchfield.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.searchfield.setPlaceholderText("Search...")
            self.searchfield.setStyleSheet("font-size: 15px; height: 20px;")

            self.searchfield.textChanged.connect(self.filter.setFilterFixedString)

            self.hBox.addWidget(self.filter_choice)
            self.hBox.addWidget(self.searchfield)

            self.table_view = QtWidgets.QTableView()
            self.table_view.setModel(self.filter)
            self.table_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

            for c in range(self.data[DataHandling.service]["columns"]):
                self.table_view.horizontalHeader().setSectionResizeMode(c, 
                    QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.vBox.addLayout(self.hBox)
            self.vBox.addWidget(self.table_view)

    def PopulateTable(self, service):
        self.data = DataHandling.command_data
        columns = self.data[service]["columns"]
        rows = self.data[f"{service}"]["rows"](f"{service}.txt")
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

# New ResultFrame class
class ResultFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("QFrame { border: 1px solid black; }")
        self.setFixedSize(1585, 250)

        # create vertical box layout
        self.v_box = QVBoxLayout(self)

        # Create an instance of ResultWidget
        self.ResultWidgetInstance = ResultWidget()

        # Add Widget to the layout
        self.v_box.addWidget(self.ResultWidgetInstance)

# _______________________________________________________________________________
# VolaGUI.py

class ParamFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setContentsMargins(5, 5, 5, 5)

        vBox = QVBoxLayout(self)

        # Create Paramaters
        param_header = QLabel("Parameters:")
        font = param_header.font()
        font.setPointSize(20)
        param_header.setFont(font)
        vBox.addWidget(param_header)

        #help

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))

        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.command_string: str
        self.check_boxes: list

        self.setWindowTitle("VolaGUI")
        self.set_window()
        #self.setStyleSheet("border: 1px solid black;") 

    def set_window(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(1)

        self.Results = ResultFrame()
        self.Description = CommandDescFrame()

        # self.Results.setStyleSheet("border: 1px solid black;") 

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


        self.param_lay = QVBoxLayout()
        self.layout.addLayout(self.param_lay, 2, 0, 1, 1)

        # Results Area
        self.layout.addWidget(self.Results, 3,0, -1, -1, 
                         alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)

        #Command Description Area
        self.layout.addWidget(self.Description, 0, 1,2,1)

        self.CommandLine = QVBoxLayout()

        # Command Building Area
        self.layout.addLayout(self.CommandLine, 2, 1,1,1)

        #Command Queue Area
        self.layout.addWidget(QueueWindow(), 0, 2,2,1)


        """
        COMMAND QUEUE AND EXECUTION BUTTONS
        """
        # Queue Command Button
        queueBtn = QPushButton(text="Queue Command", parent=self)
        queueBtn.setAutoFillBackground(True)
        queueBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        queueBtn.clicked.connect(self.queueBtnClicked)

        # Execute Command Button
        executeCMDBtn = QPushButton(text="Execute Command", parent=self)
        executeCMDBtn.setAutoFillBackground(True)
        executeCMDBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        executeCMDBtn.clicked.connect(self.executeCMDBtnClicked)

        # Execute Queue Button
        executeQUEBtn = QPushButton(text="Execute Queue", parent=self)
        executeQUEBtn.setAutoFillBackground(True)
        executeQUEBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        executeQUEBtn.clicked.connect(self.executeQUEBtnClicked)

        buttons = QVBoxLayout()
        buttons.addWidget(queueBtn)
        buttons.addWidget(executeCMDBtn)
        buttons.addWidget(executeQUEBtn)
        buttons.setSpacing(0)

        #Queue Command Button & Execute Command Button
        self.layout.addLayout(buttons, 2, 2,1,1)
        """
        COMMAND QUEUE AND EXECUTION BUTTONS
        """
        

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    # Runs when a command is clicked from the command dropdown menu
    @pyqtSlot(QTreeWidgetItem, int)
    def update_windows(self, it, col):
        command = it.text(col)
        if command in DataHandling.commands:
            if command is DataHandling.service:
                return
            DataHandling.service = command
            if command in DataHandling.supported_commands: 
                self.Description.hide()
                self.Description = CommandDescFrame()

                self.layout.addWidget(self.Description, 0, 1,2,1)
                self.command_string = f'python3 vol3.py -f mem.img windows.{DataHandling.service}' 
                self.setup_up_command_line_box(self.command_string)
                self.setup_parameters(command)
                # for i in reversed(range(self.param_lay.count())):
                #     self.param_lay.itemAt(i).widget().deleteLater()
                # Param_Header = QLabel("Parameters: ")
                # font = Param_Header.font()
                # font.setPointSize(20)
                # Param_Header.setFont(font)
                # self.param_lay.addWidget(Param_Header)
                # for param in DataHandling.command_data[f"{command}"]["params"]:
                #     c = QCheckBox(f"{param}")
                #     c.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
                #     c.stateChanged.connect(self.get_param)
                #     self.param_lay.addWidget(c)
            else:
                self.unsupported_command_error()

    def setup_parameters(self, command):
        for i in reversed(range(self.param_lay.count())):
            self.param_lay.itemAt(i).widget().deleteLater()
        Param_Header = QLabel("Parameters: ")
        font = Param_Header.font()
        font.setPointSize(20)
        Param_Header.setFont(font)
        self.param_lay.addWidget(Param_Header)
        for param in DataHandling.command_data[f"{command}"]["params"]:
            c = QCheckBox(f"{param}")
            c.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            c.stateChanged.connect(self.get_param)
            self.param_lay.addWidget(c)

    #sets up command line header and string
    def setup_up_command_line_box(self, string):
        for i in reversed(range(self.CommandLine.count())):
            self.CommandLine.itemAt(i).widget().deleteLater()
        GUI_Header = QLabel("Command Line Input: ")
        font = GUI_Header.font()
        font.setPointSize(20)
        GUI_Header.setFont(font)
        self.CommandLine.addWidget(GUI_Header)
        command_label = QLabel(self.command_string)
        font = command_label.font()
        font.setPointSize(15)
        command_label.setFont(font)
        self.CommandLine.addWidget(command_label)

    #HARDCODED
    def get_param(self):
        dialog = QInputDialog()
        dialog.setLabelText("Enter the PID: ")
        dialog.setInputMode(QInputDialog.InputMode.TextInput)
        dialog.exec()
        self.pid = dialog.textValue()
        self.command_string = f"{self.command_string} -p {self.pid}"
        self.setup_up_command_line_box(self.command_string)

    def queueBtnClicked(self):
        print("Queue Command Button Clicked")
        if DataHandling.service in DataHandling.commands:
            add_to_queue(DataHandling.service) # Replace "X" with a variable holding the name of the selected command

    def executeCMDBtnClicked(self):
        print("Execute Command Button Clicked")
        if DataHandling.service in DataHandling.supported_commands:
            self.updateResults()
        else:
            self.unsupported_command_error()

    def executeQUEBtnClicked(self):
        print("Execute Queue Button Clicked")
        execute_queue()

    def updateResults(self):
        self.Results.hide()
        self.Results = ResultFrame()
        self.Results.setStyleSheet("border: 1px solid black;") 
        self.layout.addWidget(self.Results, 3,0, -1, -1, 
                        alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)
        
    def unsupported_command_error(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ERROR")
        dlg.setText("Command not yet supported.")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

class SetUpWindow(QMainWindow):
    
    def __init__(self):
        super(SetUpWindow, self).__init__()

        self.setWindowTitle("VolaGUI Set Up")

        self.set_window()

    def set_window(self):
        self.layout = QVBoxLayout()

        # Welcome to VOLAGUI message
        messageLayout = QVBoxLayout()

        welcome = QLabel("Welcome to VOLAGUI")
        welcomeFont = welcome.font()
        welcomeFont.setPointSize(45)
        welcome.setFont(welcomeFont)
        messageLayout.addWidget(welcome)

        info = QLabel("For more information on how VOLAGUI and Volatility work, visit our Wiki on GitHub: https://github.com/volatilityfoundation/volatility/wiki")
        messageLayout.addWidget(info)

        self.layout.addLayout(messageLayout)

        # Select memory image


        # Windows Profile Button
        WindowsBtn = QPushButton(text="Windows", icon=QIcon("./icons/WindowsIcon.png"), parent=self)
        WindowsBtn.setCheckable(True)
        WindowsBtn.setAutoExclusive(True)
        WindowsBtn.setAutoFillBackground(True)
        WindowsBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        WindowsBtn.clicked.connect(self.windowsBtbClicked)

        # Mac Profile Button
        MacBtn = QPushButton(text="Mac", icon=QIcon("./icons/MacIcon"), parent=self)
        MacBtn.setCheckable(True)
        MacBtn.setAutoExclusive(True)
        MacBtn.setAutoFillBackground(True)
        MacBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        MacBtn.clicked.connect(self.macBtbClicked)

        # Linux Profile Button
        LinuxBtn = QPushButton(text="Linux", icon=QIcon("./icons/LinuxIcon"), parent=self)
        LinuxBtn.setCheckable(True)
        LinuxBtn.setAutoExclusive(True)
        LinuxBtn.setAutoFillBackground(True)
        LinuxBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        LinuxBtn.clicked.connect(self.linuxBtbClicked)

        # Create display for profile buttons
        profileButtons = QHBoxLayout()
        profileButtons.addWidget(WindowsBtn)
        profileButtons.addWidget(MacBtn)
        profileButtons.addWidget(LinuxBtn)

        self.layout.addLayout(profileButtons)

        # Start Button
        startBtn = QPushButton(text="Start", parent=self)
        startBtn.setAutoFillBackground(True)
        startBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        startBtn.clicked.connect(self.startBtnClicked)

        self.layout.addWidget(startBtn)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def windowsBtbClicked(self):
        print("Windows OS profile selected.")

    def macBtbClicked(self):
        print("Mac OS profile selected.")

    def linuxBtbClicked(self):
        print("Linux OS profile selected.")

    def startBtnClicked(self):
        print("Finished set up.")
        global window 
        window = MainWindow()
        window.showMaximized()

app = QApplication(sys.argv)
window = SetUpWindow()
window.showMaximized()
app.exec()