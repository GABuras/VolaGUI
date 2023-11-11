import sys
import QueueWidget
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget,QSizePolicy
from PyQt6 import *


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       
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

        layout = QVBoxLayout()
        layout.addWidget(queueBtn)
        layout.addWidget(executeCMDBtn)
        layout.addWidget(executeQUEBtn)
        layout.setSpacing(0)
        self.setLayout(layout)

    def queueBtnClicked(self):
        print("Queue Command Button Clicked")
        QueueWidget.add_to_queue("X") # Replace "X" with a variable holding the name of the selected command

    def executeCMDBtnClicked(self):
        print("Execute Command Button Clicked")

    def executeQUEBtnClicked(self):
        print("Execute Queue Button Clicked")