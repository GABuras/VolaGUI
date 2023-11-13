import sys
import typing

from PyQt6 import QtGui
import ResultTable
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

commands = ["moddump", "modules", "modscan", "pslist", "psscan", "pstree""hivedump", "hivelist", "hivescan"]
supported_commands = ["pslist", "psscan"]

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.check_boxes: list

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


        self.param_lay = QVBoxLayout()
        self.layout.addLayout(self.param_lay, 2, 0, 1, 1)

        # Results Area
        self.layout.addWidget(self.Results, 3,0, -1, -1, 
                         alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)

        #Command Description Area
        self.layout.addWidget(self.Description, 0, 1,2,1)

        # Command Building Area
        self.layout.addWidget(Color('purple'), 2, 1,1,1)

        #Command Queue Area
        self.layout.addWidget(QueueWidget.Window(), 0, 2,2,1)


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
        if command in commands:
            if command is DataHandling.service:
                return
            DataHandling.service = command
            if command in supported_commands: 
                self.Description.hide()
                self.Description = CommandDescription.Window()
                self.layout.addWidget(self.Description, 0, 1,2,1)
            else:
                self.unsupported_command_error()
            for i in reversed(range(self.param_lay.count())):
                self.param_lay.itemAt(i).widget().deleteLater()
            for param in DataHandling.command_data[f"{command}"]["params"]:
                c = QCheckBox(f"{param}")
                self.param_lay.addWidget(c)
                
        
    def queueBtnClicked(self):
        print("Queue Command Button Clicked")
        if DataHandling.service in commands:
            QueueWidget.add_to_queue(DataHandling.service) # Replace "X" with a variable holding the name of the selected command

    def executeCMDBtnClicked(self):
        print("Execute Command Button Clicked")
        if DataHandling.service in supported_commands:
            self.updateResults()
        else:
            self.unsupported_command_error()

    def executeQUEBtnClicked(self):
        print("Execute Queue Button Clicked")
        QueueWidget.execute_queue()

    def updateResults(self):
        self.Results.hide()
        self.Results = ResultTable.ResultWidget()
        self.layout.addWidget(self.Results, 3,0, -1, -1, 
                        alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)
        
    def unsupported_command_error(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("ERROR")
        dlg.setText("Command not yet supported.")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")
    
app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
app.exec()