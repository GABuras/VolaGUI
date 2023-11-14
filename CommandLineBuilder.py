# only needed for access to command line arguments
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


# MainWindow class inherits from QWidget
class CLBuilderWidget(QWidget):
    def __init__(self):
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


