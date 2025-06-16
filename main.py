import sys

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget

from widgets.input_section import InputSection
from widgets.output_section import OutputSection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación de Proyecto de Investigación")

        self.container = QWidget()
        containerLayout = QHBoxLayout()
        self.container.setLayout(containerLayout)

        self.input_section = InputSection()
        self.output_section = OutputSection()

        containerLayout.addWidget(self.input_section)
        containerLayout.addWidget(self.output_section)

        self.setCentralWidget(self.container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
