from PyQt5.QtWidgets import QWidget, QSpinBox, QPushButton, QGridLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QComboBox, QInputDialog, QInputDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFontDatabase, QIcon

from ui_styles_constants import *

from PyQt5 import QtWidgets, QtGui
import os

class CustomSpinBox(QWidget):
    def __init__(self, width=50, height=40, border=1, border_radious=5, font=15, font_family=None):
        super().__init__(None)
        self.spin_box = QSpinBox()
        self.spin_box.setButtonSymbols(QSpinBox.NoButtons)
        self.spin_box.setAlignment(Qt.AlignCenter)

        self.increment_button = QPushButton("▲")
        self.decrement_button = QPushButton("▼")

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
            QPushButton {{
                border-top-right-radius: {border_radious}px; 
                font-size: {font}px; 
                border-top: {border}px solid black;
                border-right: {border}px solid black;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
        """)
        self.decrement_button.setStyleSheet(f"""
            QPushButton {{
                border-bottom-right-radius: {border_radious}px; 
                font-size: {font}px; 
                border-top: {border}px solid black;
                border-right: {border}px solid black;
                border-bottom: {border}px solid black;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
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
        self.font_size = font
        self.font_family = font_family
        self.set_height = height
        self.border = border
        self.border_radious = border_radious

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
            QPushButton {{
            border-radius: {border_radious}px; 
            border: {border}px solid black; 
            background-color: #ffffff;
            font-size: {int(height*0.75)}px; 
            font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
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
        if self.checked:
            self.toggle_button.setText("X")
        else:
            self.toggle_button.setText("")

    def modifyColor(self, color_code):
        self.toggle_button.setStyleSheet(f"""
            border-radius: {self.border_radious}px; 
            border: {self.border}px solid black; 
            background-color: {color_code};
            font-size: {int(self.set_height*0.75)}px; 
            font-family: '{self.font_family}';
        """)

    def checkState(self):
        return self.checked
    
    def text(self):
        return self.label.text()

class CustomDoubleSpinBox(QWidget):
    def __init__(self, width=50, height=40, border=1, border_radious=5, font=15, font_family=None):
        super().__init__(None)
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setButtonSymbols(QSpinBox.NoButtons)
        self.spin_box.setAlignment(Qt.AlignCenter)

        self.increment_button = QPushButton("▲")
        self.decrement_button = QPushButton("▼")

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
            QPushButton {{
                border-top-right-radius: {border_radious}px; 
                font-size: {font}px; 
                border-top: {border}px solid black;
                border-right: {border}px solid black;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
        """)
        self.decrement_button.setStyleSheet(f"""
            QPushButton {{
                border-bottom-right-radius: {border_radious}px; 
                font-size: {font}px; 
                border-top: {border}px solid black;
                border-right: {border}px solid black;
                border-bottom: {border}px solid black;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
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
        self.spin_box.setValue(self.spin_box.value() + self.spin_box.singleStep())

    def decrement(self):
        self.spin_box.setValue(self.spin_box.value() - self.spin_box.singleStep())

    def setValue(self, value):
        self.spin_box.setValue(value)

    def setRange(self, minimum, maximum):
        self.spin_box.setRange(minimum, maximum)

    def setSingleStep(self, step_size):
        self.spin_box.setSingleStep(step_size)

    def value(self):
        return self.spin_box.value()
    
class CustomComboBox(QWidget):
    def __init__(self, width=100, height=40, border=1, border_radius=5, font=15, font_family=None):
        super().__init__(None)
        
        if width < 150:
            alpha = 0.75
        else:
            alpha = 0.9

        self.combo_box = QComboBox()
        self.combo_box.setEditable(True)  # To allow custom input
        self.combo_box.lineEdit().setReadOnly(True)  # Read-only like a traditional ComboBox
        self.combo_box.lineEdit().setAlignment(Qt.AlignCenter)
        self.combo_box.setFixedSize(int(alpha * width), height)

        # Hide the default dropdown button using stylesheet
        self.combo_box.setStyleSheet(f"""
            QComboBox {{
                border-top-left-radius: {border_radius}px;
                border-bottom-left-radius: {border_radius}px;
                font-size: {font}px; 
                border: {border}px solid black;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
                padding-right: 0px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 0px;
            }}
        """)

        self.dropdown_button = QPushButton("▼")
        self.dropdown_button.clicked.connect(self.toggle_popup)
        self.dropdown_button.setFixedSize(int((1-alpha) * width), height)
        self.dropdown_button.setStyleSheet(f"""
            QPushButton {{
                border-top-right-radius: {border_radius}px; 
                border-bottom-right-radius: {border_radius}px; 
                font-size: {font}px; 
                border: {border}px solid black;
                border-left: none;
                background-color: #ffffff; 
                color: #000000;
                font-family: '{font_family}';
            }}
            QPushButton:pressed {{
                background-color: #f2f2f2;
            }}
        """)

        # Layout setup
        layout = QGridLayout()
        layout.addWidget(self.combo_box, 0, 0)
        layout.addWidget(self.dropdown_button, 0, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())

    def toggle_popup(self):
        """Toggle the visibility of the combobox popup."""
        if self.combo_box.view().isVisible():
            self.combo_box.hidePopup()
        else:
            self.combo_box.showPopup()

    def addItem(self, item):
        self.combo_box.addItem(item)

    def addItems(self, items):
        self.combo_box.addItems(items)

    def currentText(self):
        return self.combo_box.currentText()

    def setCurrentIndex(self, index):
        self.combo_box.setCurrentIndex(index)

    def currentIndex(self):
        return self.combo_box.currentIndex()
    
    def setCurrentText(self, text):
        self.combo_box.setCurrentText(text)

    def count(self):
        return self.combo_box.count()
    
    def itemText(self, i):
        return self.combo_box.itemText(i)
    
    def clear(self):
        return self.combo_box.clear()