import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget,QSizePolicy
from PyQt6 import *


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       

        # Button with a text and parent widget
        queueBtn = QPushButton(text="Queue Command", parent=self)
        queueBtn.setAutoFillBackground(True)
      



        queueBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)


        # Button with an icon, a text, and a parent widget
        executeCMDBtn = QPushButton(text="Execute Command", parent=self)
        executeCMDBtn.setAutoFillBackground(True)
        executeCMDBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
       
        executeBtn = QPushButton(text="Execute Queue", parent=self)
        executeBtn.setAutoFillBackground(True)
        executeBtn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout()
        layout.addWidget(queueBtn)
        layout.addWidget(executeCMDBtn)
        layout.addWidget(executeBtn)
        layout.setSpacing(0)

        

        self.setLayout(layout)

