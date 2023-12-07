import sys
import os
import typing

from PyQt6 import QtGui, QtWidgets
# import ResultTable
# import QueueWidget
# import CommandDescription
import DataHandling
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QRect, QSortFilterProxyModel, QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


global window
# setting up connection comment
# _______________________________________________________________________________
# CommandDecription.py

class CommandDescFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.generate_description()
        self.setStyleSheet("QFrame { border: 1px solid black; border-style: outset;}")
        self.setFixedSize(900, 450)

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

        font = queue.font()
        font.setPointSize(15)
        queue.setFont(font)
        
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
        self.smallVBox = QtWidgets.QVBoxLayout()
        self.vBox.addStretch(0)
        self.vBox.setSpacing(0)
        self.setLayout(self.vBox)
        self.hBox = QtWidgets.QHBoxLayout()
        self.hBox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if DataHandling.service is not None:
            self.PopulateTable(DataHandling.service)
            self.label = QLabel(f"{DataHandling.service} Results:")
            self.label.setFixedWidth(150)
            self.label.setStyleSheet("border: 0px;")
            font = QFont()
            font.setPointSize(16)
            self.label.setFont(font)
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

            self.smallVBox.addWidget(self.label)
            
            self.hBox.addWidget(self.filter_choice)
            self.hBox.addWidget(self.searchfield)

            self.table_view = QtWidgets.QTableView()
            self.table_view.setModel(self.filter)
            self.table_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)

            for c in range(self.data[DataHandling.service]["columns"]):
                self.table_view.horizontalHeader().setSectionResizeMode(c, 
                    QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.smallVBox.addLayout(self.hBox)
            self.vBox.addLayout(self.smallVBox)
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
        self.setFixedHeight(250)

        # create vertical box layout
        self.v_box = QVBoxLayout(self)

        # Create an instance of ResultWidget
        self.ResultWidgetInstance = ResultWidget()

        # Add Widget to the layout
        self.v_box.addWidget(self.ResultWidgetInstance)

# _______________________________________________________________________________
# VolaGUI.py

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
        font = queueBtn.font()
        font.setPointSize(15)
        queueBtn.setFont(font)

        # Execute Command Button
        executeCMDBtn = QPushButton(text="Execute Command", parent=self)
        executeCMDBtn.setAutoFillBackground(True)
        executeCMDBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        executeCMDBtn.clicked.connect(self.executeCMDBtnClicked)
        executeCMDBtn.setFont(font)

        # Execute Queue Button
        executeQUEBtn = QPushButton(text="Execute Queue", parent=self)
        executeQUEBtn.setAutoFillBackground(True)
        executeQUEBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        executeQUEBtn.clicked.connect(self.executeQUEBtnClicked)
        executeQUEBtn.setFont(font)

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
                self.command_parameters = ""
                self.setup_up_command_line_box()
                self.setup_parameters(command)
            else:
                self.unsupported_command_error()

    def setup_parameters(self, command):
        for i in reversed(range(self.param_lay.count())):
            if i == 0:
                self.param_lay.itemAt(i).widget().deleteLater()
            else:
                for j in reversed(range(self.param_lay.itemAt(i).layout().count())):
                    self.param_lay.itemAt(i).layout().itemAt(j).widget().deleteLater()
                self.param_lay.itemAt(i).layout().deleteLater()
        Param_Header = QLabel("Parameters: ")
        Param_Header.setAlignment(Qt.AlignmentFlag.AlignTop)
        font = Param_Header.font()
        font.setPointSize(20)
        Param_Header.setFont(font)
        
        self.param_lay.addWidget(Param_Header)
        for param in DataHandling.command_data[f"{command}"]["params"]:
            # c = QCheckBox(f"{param}")
            # c.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            # c.stateChanged.connect(self.get_param)
            # self.param_lay.addWidget(c)
            paramLayout = QHBoxLayout()
            
            paramLabel = QLabel(f"{param}")
            paramLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            paramLabel.setFixedWidth(50)
            font.setPointSize(15)
            paramLabel.setFont(font)
            paramLayout.addWidget(paramLabel)

            self.paramEditBox = QLineEdit()
            self.paramEditBox.textChanged.connect(self.update_param)
            self.paramEditBox.setFixedWidth(175)
            self.paramEditBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            paramLayout.addWidget(self.paramEditBox)

            self.spacing = QLabel("")
            paramLayout.addWidget(self.spacing)

            paramLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.param_lay.addLayout(paramLayout)

    #sets up command line header and string
    def setup_up_command_line_box(self):
        for i in reversed(range(self.CommandLine.count())):
            self.CommandLine.itemAt(i).widget().deleteLater()
        GUI_Header = QLabel("Command Line Input: ")
        font = GUI_Header.font()
        font.setPointSize(20)
        GUI_Header.setFont(font)
        GUI_Header.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.CommandLine.addWidget(GUI_Header)
        command_label = QLabel(self.command_string + self.command_parameters)
        font = command_label.font()
        font.setPointSize(15)
        command_label.setFont(font)
        command_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.CommandLine.addWidget(command_label)

    #HARDCODED
    # def get_param(self):
    #     dialog = QInputDialog()
    #     dialog.setLabelText("Enter the PID: ")
    #     dialog.setInputMode(QInputDialog.InputMode.TextInput)
    #     dialog.exec()
    #     self.pid = dialog.textValue()
    #     self.command_string = f"{self.command_string} -p {self.pid}"
    #     self.setup_up_command_line_box(self.command_string)

    #HARDCODED
    def update_param(self):
        if self.paramEditBox.text() != "":
            self.command_parameters = " -p " + str(self.paramEditBox.text())
        else:
            self.command_parameters = ""
        self.setup_up_command_line_box()

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
        print("Unsupported command error.")
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
        welcome.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        welcome.setFixedHeight(60)
        messageLayout.addWidget(welcome)

        info = QLabel("For more information on how VOLAGUI and Volatility work, visit our Wiki on GitHub: https://github.com/volatilityfoundation/volatility/wiki")
        regFont = info.font()
        regFont.setPointSize(15)
        info.setFont(regFont)
        info.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        info.setFixedHeight(100)
        messageLayout.addWidget(info)

        self.layout.addLayout(messageLayout)

        # Select memory image
        self.imageSelectedFlag = False

        selectLayout = QHBoxLayout()
        
        spacing = QLabel("")
        spacing.setFixedWidth(100)
        spacing.setFixedHeight(100)
        selectLayout.addWidget(spacing)

        selectMessage = QLabel("Memory Image:")
        selectMessage.setFont(regFont)
        selectMessage.setFixedWidth(150)
        selectMessage.setFixedHeight(100)
        selectLayout.addWidget(selectMessage)

        imageBtn = QPushButton(text="Select a Memory Image")
        imageBtn.clicked.connect(self.imageBtnClicked)
        imageBtn.setFixedWidth(250)
        imageBtn.setFixedHeight(50)

        selectLayout.addWidget(imageBtn)

        self.selectedImage = QLabel("No memory image selected")
        self.selectedImage.setFont(regFont)
        self.selectedImage.setFixedHeight(100)

        selectLayout.addWidget(self.selectedImage)

        self.layout.addLayout(selectLayout)

        # Select Profile
        selectProfileMessage = QLabel("Select the Memory Image Type: ")
        selectProfileMessage.setFont(regFont)
        selectProfileMessage.setFixedHeight(30)
        self.layout.addWidget(selectProfileMessage)

        # Select Profile Buttons

        # Windows Profile Button
        self.profileSelectedFlag = False

        WindowsBtn = QPushButton(text="   Windows", icon=QIcon("./icons/WindowsIcon.png"), parent=self)
        WindowsBtn.setCheckable(True)
        WindowsBtn.setAutoExclusive(True)
        WindowsBtn.setAutoFillBackground(True)
        WindowsBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        WindowsBtn.setIconSize(QSize(150,150))
        profileBtnFont = WindowsBtn.font()
        profileBtnFont.setPointSize(30)
        WindowsBtn.setFont(profileBtnFont)
        WindowsBtn.clicked.connect(self.windowsBtnClicked)

        # Mac Profile Button
        MacBtn = QPushButton(text=" Mac", icon=QIcon("./icons/MacIcon"), parent=self)
        MacBtn.setCheckable(True)
        MacBtn.setAutoExclusive(True)
        MacBtn.setAutoFillBackground(True)
        MacBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        MacBtn.setIconSize(QSize(150,150))
        MacBtn.setFont(profileBtnFont)
        MacBtn.clicked.connect(self.macBtnClicked)

        # Linux Profile Button
        LinuxBtn = QPushButton(text="Linux", icon=QIcon("./icons/LinuxIcon"), parent=self)
        LinuxBtn.setCheckable(True)
        LinuxBtn.setAutoExclusive(True)
        LinuxBtn.setAutoFillBackground(True)
        LinuxBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        LinuxBtn.setIconSize(QSize(200,200))
        LinuxBtn.setFont(profileBtnFont)
        LinuxBtn.clicked.connect(self.linuxBtnClicked)

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
        startBtn.setFont(profileBtnFont)
        startBtn.setFixedHeight(150)
        startBtn.clicked.connect(self.startBtnClicked)

        self.layout.addWidget(startBtn)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def imageBtnClicked(self):
        print("Select memory image button clicked.")
        response = self.getFileName()
        if response[0] != "":
            self.selectedImage.setText(str(response[0]))
            self.imageSelectedFlag = True
        else:
            self.selectedImage.setText("No memory image selected")
            self.imageSelectedFlag = False

    def getFileName(self):
        file_filter = 'Memory Image (*.raw *.vmem *.img)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a memory image',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Memory Image (*.raw *.vmem *.img)'
        )
        return response

    def windowsBtnClicked(self):
        print("Windows OS profile selected.")
        self.profileSelectedFlag = True

    def macBtnClicked(self):
        print("Mac OS profile selected.")
        self.profileSelectedFlag = True

    def linuxBtnClicked(self):
        print("Linux OS profile selected.")
        self.profileSelectedFlag = True

    def startBtnClicked(self):
        print("Start button clicked.")
        if self.imageSelectedFlag == True and self.profileSelectedFlag == True:
            global window 
            window = MainWindow()
            window.showMaximized()
        else:
            self.must_select_error()

    def must_select_error(self):
        print("Must choose a memory image and a profile to continue.")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ERROR")
        dlg.setText("Must select a memory image and a profile.")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

app = QApplication(sys.argv)
window = SetUpWindow()
window.showMaximized()
app.exec()