import sys
import ResultTable
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


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

        self.setWindowTitle("VolGUI")

        layout = QGridLayout()
        layout.setSpacing(1)


        #Select and Show Command Area 
        layout.addWidget(Color('red'), 0, 0,3,1)

        # Results Area
        layout.addWidget(ResultTable.ResultWidget("pslist"), 3,0, -1, -1, 
                         alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)

        #Command Description Area
        layout.addWidget(Color('blue'), 0, 1,2,1)

        # Command Building Area
        layout.addWidget(Color('purple'), 2, 1,1,1)

        #Command Queque Area
        layout.addWidget(Color('green'), 0, 2,2,1)

        #Queue Command Button
        layout.addWidget(Color('yellow'), 1, 2,1,1)

        #Execute Command Button
        layout.addWidget(Color('black'), 2, 2,1,1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()