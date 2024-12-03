from PyQt5.QtWidgets import QWidget, QSpinBox, QPushButton, QGridLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CustomSpinBox(QWidget):
    def __init__(self, width=50, height=40, border=1, border_radious=5, font=15, font_family=None):
        super().__init__(None)
        self.spin_box = QSpinBox()
        self.spin_box.setButtonSymbols(QSpinBox.NoButtons)
        self.spin_box.setAlignment(Qt.AlignCenter)

        self.increment_button = QPushButton("+")
        self.decrement_button = QPushButton("-")

        self.increment_button.clicked.connect(self.increment)
        self.decrement_button.clicked.connect(self.decrement)

        self.spin_box.setFixedSize(int(1.25*width//2), height)
        self.increment_button.setFixedSize(int(0.75*width//2), height//2)
        self.decrement_button.setFixedSize(int(0.75*width//2), height//2)
        self.spin_box.setStyleSheet(f"""
            border-top-left-radius: {border_radious}px;
            border-bottom-left-radius: {border_radious}px;
            font-size: {font}px; 
            border: {border}px solid black;
            background-color: #ffffff; 
            color: #000000;
            font-family: '{font_family}';
        """)
        self.increment_button.setStyleSheet(f"""
            border-top-right-radius: {border_radious}px; 
            font-size: {font}px; 
            border-top: {border}px solid black;
            border-right: {border}px solid black;
            background-color: #ffffff; 
            color: #000000;
            font-family: '{font_family}';
        """)
        self.decrement_button.setStyleSheet(f"""
            border-bottom-right-radius: {border_radious}px; 
            font-size: {font}px; 
            border-top: {border}px solid black;
            border-right: {border}px solid black;
            border-bottom: {border}px solid black;
            background-color: #ffffff; 
            color: #000000;
            font-family: '{font_family}';
        """)

        layout = QGridLayout()
        layout.addWidget(self.spin_box, 0, 0, 2, 1)
        layout.addWidget(self.increment_button, 0, 1)
        layout.addWidget(self.decrement_button, 1, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())

        self.setRange(0, 100)
        self.setValue(0)

    def increment(self):
        self.spin_box.setValue(self.spin_box.value() + 1)

    def decrement(self):
        self.spin_box.setValue(self.spin_box.value() - 1)

    def setValue(self, value):
        self.spin_box.setValue(value)

    def setRange(self, minimum, maximum):
        self.spin_box.setRange(minimum, maximum)

    def value(self):
        return self.spin_box.value()

class CustomCheckBox(QWidget):
    def __init__(self, text='', width=150, height=40, border=1, border_radious=5, font=15, font_family=None):
        super().__init__(None)
        
        self.checked = False

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setFixedSize(width, height)
        self.label.setStyleSheet(f"""
            font-size: {font}px; 
            background-color: #ffffff; 
            color: #000000; 
            font-family: '{font_family}';
        """)

        self.toggle_button = QPushButton()
        self.toggle_button.setFixedSize(height, height)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet(f"""
            border-radius: {border_radious}px; 
            border: {border}px solid black; 
            background-color: #ffffff;
            font-size: {int(height*0.75)}px; 
            font-family: '{font_family}';
        """)

        self.toggle_button.clicked.connect(self.toggle)

        layout = QHBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(font//2)

        self.setLayout(layout)
        self.setFixedSize(layout.sizeHint())

    def toggle(self):
        self.checked = not self.checked
        if self.checked:
            self.toggle_button.setText("X")
        else:
            self.toggle_button.setText("")

    def isChecked(self):
        return self.checked

    def setText(self, text):
        self.label.setText(text)

    def setChecked(self, state):
        self.checked = state
        self.toggle_button.setChecked(state)
        self.toggle()