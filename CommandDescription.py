import sys

from PyQt6.QtCore import *
from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget,QSizePolicy,QLineEdit,QHBoxLayout,QLayout
from PyQt6 import *
from DataHandling import command_data
class Window(QWidget):

    def __init__(self, service):
        super().__init__()

        header = QLabel(f"Command Description: {service}")
        font = header.font()
        font.setPointSize(20)
        header.setFont(font)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setScaledContents(False)
        header.setFixedHeight(35)
        self.data = command_data
        headerlayout = QHBoxLayout()
        headerlayout.addWidget(header)


    #https://code.google.com/archive/p/volatility/wikis/CommandReference22.wiki#:~:text=Processes%20and%20DLLs-,pslist,the%20process%20started%20and%20exited.

        #psScanDescription = "\nTo enumerate processes using pool tag scanning, use the psscan command. This can find processes that previously terminated (inactive) and processes that have been hidden or unlinked by a rootkit."

        #psScanCommandInfo = "Volatility 3 Framework 2.4.1\nusage: volatility windows.psscan.PsScan [-h] [--pid [PID ...]] [--dump] [--physical]\noptions:\n-h, --help       show this help message and exit\n--pid [PID ...]  Process ID to include (all other processes are excluded)\n--dump           Extract listed processes\n--physical       Display physical offset instead of virtual"

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

      

        layout = QVBoxLayout()
    
        layout.addLayout(headerlayout)

        layout.addWidget(description)
        
        layout.addWidget(CommandInfo)

        layout.setSpacing(0)

        self.setLayout(layout)
        
