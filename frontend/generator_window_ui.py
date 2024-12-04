from PyQt5 import QtCore, QtGui, QtWidgets
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout, QTextEdit, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

from frontend.custom_classes import CustomSpinBox, CustomCheckBox, CustomComboBox

class Ui_generate_images(object):
    def __init__(self, config, ui_styles):
        self.config = config
        self.ui_styles = ui_styles

    def setupUi(self, GeneratorWindow):
        GeneratorWindow.setObjectName("GenerateImgs")
        
        self.centralwidget = QtWidgets.QWidget(GeneratorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_grid = QtWidgets.QGridLayout(self.centralwidget)

        regular_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

        # Top Section - Return button and Title
        self.setup_top_section()

        # Left Section - Form controls
        self.setup_left_section()

        # Right Section - Image Preview and Progress Bar
        self.setup_right_section()

        # Bottom Section - Buttons
        self.setup_bottom_buttons()

        self.left_layout.setContentsMargins(self.ui_styles[PADDINGS][SIDES], 0, self.ui_styles[PADDINGS][SIDES]//2, 0)
        self.right_layout.setContentsMargins(self.ui_styles[PADDINGS][SIDES]//2, 0, self.ui_styles[PADDINGS][SIDES], 0)

        GeneratorWindow.setCentralWidget(self.centralwidget)
        GeneratorWindow.setWindowTitle("IMGEAN")

        self.load_models()  # Load models from configuration
        self.load_quality_checks()  # Load quality checks from configuration
        GeneratorWindow.load_initial_values()  # Load initial values from config

    def setup_top_section(self):
        # General top layout
        self.top_section_layout = QtWidgets.QGridLayout()
        self.top_section_layout.setContentsMargins(0, 0, 0, 0)
        self.top_section_layout.setSpacing(0)

        # This are weights for each column, so we can center the title
        self.top_section_layout.setColumnStretch(0, 1)  # Left side
        self.top_section_layout.setColumnStretch(1, 2)  # Center column
        self.top_section_layout.setColumnStretch(2, 1)  # Right side

        # Return Button in the Top-Left
        return_button = QPushButton("Return")
        return_button.setFixedSize(
            self.ui_styles[SIZES][RETURN_BUTTON][WIDTH],
            self.ui_styles[SIZES][RETURN_BUTTON][HEIGHT]
        )
        return_button.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][ORANGE]}; 
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][ORANGE_PRESSED]};
            }}
        """)
        self.return_button = return_button
        self.top_section_layout.addWidget(self.return_button, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Title Fully Centered
        title = QLabel("Generate images")
        bold_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][BOLD_FONT_FILE])
        bold_font_family = QFontDatabase.applicationFontFamilies(bold_font_id)[0]
        title.setStyleSheet(f"""
            font-family: '{bold_font_family}';
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]}px;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.top_section_layout.addWidget(title, 0, 1, alignment=Qt.AlignCenter)

        # Add the top section layout to the main grid
        self.main_grid.addLayout(self.top_section_layout, 0, 0, 1, 2)

    def setup_left_section(self):
        """Setup the left section with form controls."""
        self.left_layout = QtWidgets.QFormLayout()
        self.left_layout.setSpacing(self.ui_styles[PADDINGS][SPACING_AMONG_ELEMENTS])

        # Prompt Input (Directly set text from config)
        label_prompt = QLabel("Prompt:")
        label_prompt.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)

        text_prompt = QTextEdit()
        text_prompt.setText(self.config[GENERATION][PROMPTS][POSITIVE])
        text_prompt.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        text_prompt.setFixedHeight(self.ui_styles[SIZES][PROMPT_BOX][HEIGHT])
        self.text_prompt = text_prompt

        self.left_layout.addRow(label_prompt, text_prompt)

        # Negative Prompt Input (Directly set text from config)
        label_negative_prompt = QLabel("Negative Prompt:")
        label_negative_prompt.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)

        text_negative_prompt = QTextEdit()
        text_negative_prompt.setText(self.config[GENERATION][PROMPTS][POSITIVE])
        text_negative_prompt.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        text_negative_prompt.setFixedHeight(self.ui_styles[SIZES][PROMPT_BOX][HEIGHT])
        self.text_negative_prompt = text_negative_prompt

        self.left_layout.addRow(label_negative_prompt, self.text_negative_prompt)

        # Create a horizontal layout for the row
        self.row_layout = QtWidgets.QGridLayout()

        # Number of images
        label_images = QLabel("Num. images:")
        label_images.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)

        self.spin_images = CustomSpinBox(width=self.ui_styles[SIZES][GENERATION_SPINBOX][WIDTH], 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)

        self.spin_images.setRange(1, 100)

        self.row_layout.addWidget(label_images, 0, 0)
        self.row_layout.addWidget(self.spin_images, 0, 1)
        self.row_layout.setAlignment(label_images, QtCore.Qt.AlignRight)
        self.row_layout.setAlignment(self.spin_images, QtCore.Qt.AlignLeft)

        # Steps
        label_steps = QLabel("Num. steps:")
        label_steps.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)

        self.spin_steps = CustomSpinBox(width=self.ui_styles[SIZES][GENERATION_SPINBOX][WIDTH]-5, 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)

        self.spin_steps.setRange(1, 50)

        self.row_layout.addWidget(label_steps, 0, 2)
        self.row_layout.addWidget(self.spin_steps, 0, 3)
        self.row_layout.setAlignment(label_steps, QtCore.Qt.AlignRight)
        self.row_layout.setAlignment(self.spin_steps, QtCore.Qt.AlignLeft)

        # Seed
        label_seed = QLabel("Seed:")
        label_seed.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)

        self.text_seed = QtWidgets.QLineEdit()
        self.text_seed.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        self.text_seed.setValidator(QtGui.QIntValidator())
        self.text_seed.setPlaceholderText("Optional")
        self.text_seed.setAlignment(Qt.AlignCenter)
        self.text_seed.setFixedWidth(self.ui_styles[SIZES][SEED_BOX][WIDTH])
        self.text_seed.setMaximumWidth(self.ui_styles[SIZES][SEED_BOX][WIDTH])

        self.row_layout.addWidget(label_seed, 0, 4)
        self.row_layout.addWidget(self.text_seed, 0, 5)
        self.row_layout.setAlignment(label_seed, QtCore.Qt.AlignRight)
        self.row_layout.setAlignment(self.text_seed, QtCore.Qt.AlignLeft)

        for col in range(6):
            self.row_layout.setColumnStretch(col, 1)

        # Add the horizontal layout to your main layout
        self.left_layout.addRow(self.row_layout)

        self.model_filename_layout = QtWidgets.QGridLayout()

        # Model selection
        label_model = QLabel("Model:")
        label_model.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)
        self.combo_model = self.defaultColorComboBox = CustomComboBox(width=self.ui_styles[SIZES][COMBO_MODELS][WIDTH], 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radius=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)

        self.model_filename_layout.addWidget(label_model, 0, 0)
        self.model_filename_layout.addWidget(self.combo_model, 0, 1)
        self.model_filename_layout.setAlignment(label_model, QtCore.Qt.AlignRight)
        self.model_filename_layout.setAlignment(self.combo_model, QtCore.Qt.AlignLeft)

        # File Name 
        label_filename = QLabel("File Name:")
        label_filename.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)
        self.text_filename = QtWidgets.QLineEdit()
        self.text_filename.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        self.text_filename.setAlignment(Qt.AlignCenter)
        self.text_filename.setText(self.config[GENERATION][FILENAME])
        self.text_filename.setPlaceholderText("Enter filename")
        self.text_filename.editingFinished.connect(self.validate_filename)
        self.text_filename.setFixedWidth(150)

        self.model_filename_layout.addWidget(label_filename, 0, 2)
        self.model_filename_layout.addWidget(self.text_filename, 0, 3)

        self.model_filename_layout.setAlignment(label_filename, QtCore.Qt.AlignRight)
        self.model_filename_layout.setAlignment(self.text_filename, QtCore.Qt.AlignLeft)

        self.model_filename_layout.setColumnStretch(1, 1)  # Middle column 1 (expand)
        self.model_filename_layout.setColumnStretch(2, 1)  # Middle column 2 (expand)

        self.model_filename_layout.setColumnStretch(0, 0)  # First column (no expansion)
        self.model_filename_layout.setColumnStretch(3, 0)  # Last column (no expansion)

        self.left_layout.addRow(self.model_filename_layout)

        # Manual Quality Check
        self.checkbox_manual = CustomCheckBox(text="Manual Quality Check",
                                              width=self.ui_styles[SIZES][GENERATION_MANUAL_CHECKBOX][WIDTH], 
                                              height=self.ui_styles[SIZES][GENERATION_MANUAL_CHECKBOX][HEIGHT], 
                                              border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                              border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                              font=self.ui_styles[FONTS][LABEL_FONT_SIZE],
                                              font_family=self.regular_font_family)
        self.left_layout.addRow(self.checkbox_manual)

        # Quality Checks
        label_auto_check = QLabel("Automatic Quality Check:")
        label_auto_check.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)
        self.auto_check_list = QtWidgets.QListWidget()
        self.auto_check_list.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
                padding: {self.ui_styles[PADDINGS][LIST_DEFAULT_PADDING]}px;
            }}
            QListWidget::item {{
                margin-bottom: {self.ui_styles[PADDINGS][LABELS_UP]}px;
            }}
            QScrollBar:vertical {{              
                width:{self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop: 0 {self.ui_styles[COLORS][BLACK]}, stop: 0.5 {self.ui_styles[COLORS][BLACK]}, stop:1 {self.ui_styles[COLORS][BLACK]});
                min-height: 0px;
            }}
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0 px;
            }}
        """)
        self.auto_check_list.setFixedHeight(self.ui_styles[SIZES][AUTO_CHECK_LIST][HEIGHT])
        self.auto_check_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.left_layout.addRow(label_auto_check, self.auto_check_list)

        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_layout.addItem(spacer)

        self.main_grid.addLayout(self.left_layout, 1, 0)

    def setup_right_section(self):
        """Setup the right section with image preview and progress bar."""
        self.right_layout = QtWidgets.QVBoxLayout()
        # Setup QGraphicsView with scene
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphics_view.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        self.graphics_view.setScene(QtWidgets.QGraphicsScene(self.graphics_view))
        self.graphics_view.setAlignment(QtCore.Qt.AlignCenter)
        self.graphics_view.setFixedSize(self.ui_styles[SIZES][GENERATOR_GRAPHIC_VIEW][WIDTH], self.ui_styles[SIZES][GENERATOR_GRAPHIC_VIEW][HEIGHT])
        self.graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.right_layout.addWidget(self.graphics_view)
        # Setup a simple progress bar
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
                text-align: center; 
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
            }}
            QProgressBar::chunk {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}  
        """) # TODO see how to put borders
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)  # Start at 0
        self.progress_bar.setTextVisible(True)  # Make the text visible
        self.right_layout.addWidget(self.progress_bar)

        self.main_grid.addLayout(self.right_layout, 1, 1)

    def setup_bottom_buttons(self):
        """Setup the bottom buttons (Cancel and Generate)."""
        self.button_layout = QtWidgets.QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        # btn_cancel.setFixedSize(main_button_width, main_button_height)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]};
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
        """)
        self.cancel_button = cancel_button

        self.button_layout.addWidget(self.cancel_button)

        generate_button = QPushButton("Generate")
        # btn_cancel.setFixedSize(main_button_width, main_button_height)
        generate_button.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]};
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.generate_button = generate_button

        self.button_layout.addWidget(self.generate_button)

        self.right_layout.addLayout(self.button_layout)

    def load_models(self):
        """Load models from the configuration into the combo box."""
        models = self.config.get('GENERATION', {}).get('MODELS', [])
        for model in models:
            self.combo_model.addItem(model['name'])

    def load_quality_checks(self):
        """Load quality checks from the configuration into the list."""
        functions = self.config.get('QUALITY_CHECKS', {}).get('FUNCTIONS', [])
        for func in functions:
            custom_checkBox = CustomCheckBox(text=func['name'],
                                  width=self.ui_styles[SIZES][DEFAULT_CHECKBOX][WIDTH], 
                                  height=self.ui_styles[SIZES][DEFAULT_CHECKBOX][HEIGHT],  
                                  border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                  border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                  font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                  font_family=self.regular_font_family)
            item = QtWidgets.QListWidgetItem()

            self.auto_check_list.addItem(item)
            self.auto_check_list.setItemWidget(item, custom_checkBox)

            # item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            # item.setCheckState(QtCore.Qt.Unchecked)
            # self.auto_check_list.addItem(item)

    def validate_filename(self):
        """Validate the filename input and update the configuration."""
        filename = self.text_filename.text().strip()
        
        # If the filename is empty, restore the last saved value
        if not filename:
            previous_filename = self.config['GENERATION'].get('filename', 'generated_image')
            self.text_filename.setText(previous_filename)
        else:
            # Save the new filename to the configuration
            self.config['GENERATION']['filename'] = filename
            self.save_config()