import sys

from PyQt6.QtCore import *
from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget,QSizePolicy,QLineEdit,QHBoxLayout,QLayout
from PyQt6 import *


class Window(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        

        header = QLabel("Queue:")
        font = header.font()
        font.setPointSize(20)
        header.setFont(font)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setScaledContents(False)
        header.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        command = QLineEdit()
        command.setPlaceholderText("<Command>")
        command.setReadOnly(True)
        command.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        headerlayout = QHBoxLayout()
        headerlayout.addWidget(header)
        headerlayout.addWidget(command)
        
        global queue # Necessary to allow the button click handling code in ButtonWidget.py to update queue contents. Fix if you know how to
        queue = QListWidget()
        # Placeholder text would be ideal, but seems a little complicated, so maybe do later
        
        # queue.addItems(["One", "Two", "Three"])

        queue.currentItemChanged.connect(self.index_changed)
        queue.currentTextChanged.connect(self.text_changed)
        queue.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)


        layout = QVBoxLayout()
    
        layout.addLayout(headerlayout)

        layout.addWidget(queue)
        layout.setSpacing(0)



        self.setLayout(layout)
        


    def index_changed(self, i): # Not an index, i is a QListWidgetItem
        print(i.text())

    def text_changed(self, s): # s is a str
        print(s)

def add_to_queue(command: str): # command is the name of the command
    queue.addItem(command)
    print("Added " + command + " to queue")

def execute_queue(): 
    # for command in queue, execute and display results
    queue.clear()
    print("Executed queue")