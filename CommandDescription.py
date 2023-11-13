import sys

from PyQt6.QtCore import *
from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget,QSizePolicy,QLineEdit,QHBoxLayout,QLayout
from PyQt6 import *
import DataHandling
class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.generate_description()

    def generate_description(self):
        service = DataHandling.service
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

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
        
        layout.addLayout(headerlayout)
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

        layout.addWidget(description)
            
        layout.addWidget(CommandInfo)
