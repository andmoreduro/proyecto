from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget


class SingleLineTextInputGroup(QWidget):
    def __init__(self, label: str = "Label", placeholder: str = "Placeholder"):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.label = QLabel(label)
        self.layout().addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.layout().addWidget(self.input)


class MultiLineTextInputGroup(QWidget):
    def __init__(self, label: str = "Label", placeholder: str = "Placeholder"):
        super().__init__()

        self.setLayout(QVBoxLayout())

        self.label = QLabel(label)
        self.layout().addWidget(self.label)

        self.input = QTextEdit()
        self.input.setPlaceholderText(placeholder)
        self.layout().addWidget(self.input)
