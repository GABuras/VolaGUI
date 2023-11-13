import sys

from PyQt6.QtCore import *
from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget,QSizePolicy,QLineEdit,QHBoxLayout,QLayout
from PyQt6 import *

class Window(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        header = QLabel("Command Description: PsList")
        font = header.font()
        font.setPointSize(20)
        header.setFont(font)
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setScaledContents(False)
        header.setFixedHeight(35)

        headerlayout = QHBoxLayout()
        headerlayout.addWidget(header)


    #https://code.google.com/archive/p/volatility/wikis/CommandReference22.wiki#:~:text=Processes%20and%20DLLs-,pslist,the%20process%20started%20and%20exited.

        psListDescription = "\nTo list the processes of a system, use the pslist command. This walks the doubly-linked list pointed to by PsActiveProcessHead and shows the offset, process name, process ID, the parent process ID, number of threads, number of handles, and date/time when the process started and exited. This plugin does not detect hidden or unlinked processes (but psscan can do that)."
       
        psListCommandInfo = "Volatility 3 Framework 2.4.1\nusage: volatility windows.pslist.PsList [-h] [--physical] [--pid [PID ...]] [--dump]\noptions:\n-h, --help       show this help message and exit\n--physical       Display physical offsets instead of virtual\n--pid [PID ...]  Process ID to include (all other processes are excluded)\n--dump           Extract listed processes"

        psScanDescription = "\nTo enumerate processes using pool tag scanning, use the psscan command. This can find processes that previously terminated (inactive) and processes that have been hidden or unlinked by a rootkit."

        psScanCommandInfo = "Volatility 3 Framework 2.4.1\nusage: volatility windows.psscan.PsScan [-h] [--pid [PID ...]] [--dump] [--physical]\noptions:\n-h, --help       show this help message and exit\n--pid [PID ...]  Process ID to include (all other processes are excluded)\n--dump           Extract listed processes\n--physical       Display physical offset instead of virtual"

        description = QLabel(psScanDescription)
        font = description.font()
        font.setPointSize(15)
        description.setFont(font)
        description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        description.setScaledContents(False)
        description.setWordWrap(True) 

        CommandInfo = QLabel(psScanCommandInfo)
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
        
