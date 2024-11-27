from PyQt5 import QtCore, QtGui, QtWidgets
import backend.annotation_manager.dataset_utils as du

from PyQt5 import QtCore, QtGui, QtWidgets
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

class Ui_AnnotateImg(object):
    def __init__(self, config, ui_styles):
        self.config = config
        self.dataset_manager = du.DatasetManager(config["DATASET"]["PATH"], config)
        self.ui_styles = ui_styles

        regular_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

    def setupUi(self, AnnotateImg):
        AnnotateImg.setObjectName("CheckImgQuality")
        
        self.centralwidget = QtWidgets.QWidget(AnnotateImg)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, self.ui_styles[PADDINGS][MIN_SIDES], self.ui_styles[PADDINGS][MIN_SIDES])

        # Title and Return Button (Top Section)
        self.setup_top_section()

        self.setup_left_layout()

        self.setup_right_layout()

        self.setup_dropdown_menu()

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(2, 1)

        AnnotateImg.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(AnnotateImg)
    
    def setup_top_section(self):
        # General top layout
        self.top_section_layout = QtWidgets.QGridLayout()
        self.top_section_layout.setContentsMargins(0, 5, 0, 0)
        self.top_section_layout.setSpacing(0)

        # This are weights for each column, so we can center the title
        self.top_section_layout.setColumnStretch(0, 1)  # Left side
        self.top_section_layout.setColumnStretch(1, 2)  # Center column
        self.top_section_layout.setColumnStretch(2, 1)  # Right side

        # Return Button in the Top-Left
        returnButton = QPushButton("Return")
        returnButton.setFixedSize(
            self.ui_styles[SIZES][RETURN_BUTTON][WIDTH],
            self.ui_styles[SIZES][RETURN_BUTTON][HEIGHT]
        )
        returnButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][ORANGE]}; 
        """)
        self.returnButton = returnButton
        self.top_section_layout.addWidget(self.returnButton, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Title Fully Centered
        title = QLabel("Check image quality")
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
        self.main_layout.addLayout(self.top_section_layout, 0, 0, 1, 3)

    def setup_left_layout(self):
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout(self.left_widget)
        self.left_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.left_layout.setSpacing(self.ui_styles[PADDINGS][SPACING_AMONG_ELEMENTS])

        # Image Placeholder (This will display the image to annotate)
        self.imageLabel = QtWidgets.QLabel("No images to annotate")
        self.imageLabel.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        self.imageLabel.setFixedSize(self.ui_styles[SIZES][ANNOTATE_IMG][HEIGHT],self.ui_styles[SIZES][ANNOTATE_IMG][WIDTH])
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.left_layout.addWidget(self.imageLabel)

        self.nav_button_layout = QtWidgets.QHBoxLayout()

        # Navigation buttons below the image
        self.prevButton = QtWidgets.QPushButton("Prev")
        self.prevButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
        """)
        self.prevButton.setFixedWidth(self.ui_styles[SIZES][LABEL_NAV_BUTTON][WIDTH])

        self.nav_button_layout.addWidget(self.prevButton)

        self.discardButton = QtWidgets.QPushButton("Discard")
        self.discardButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
        """)
        self.discardButton.setFixedWidth(self.ui_styles[SIZES][LABEL_NAV_BUTTON][WIDTH]*2)

        self.nav_button_layout.addWidget(self.discardButton)

        self.nextButton = QtWidgets.QPushButton("Next")
        self.nextButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
        """)
        self.nextButton.setFixedWidth(self.ui_styles[SIZES][LABEL_NAV_BUTTON][WIDTH])
        self.nav_button_layout.addWidget(self.nextButton)

        self.left_layout.addLayout(self.nav_button_layout)

        self.main_layout.addWidget(self.left_widget, 1, 1, 1, 1)

    def setup_right_layout(self):

        self.right_layout = QtWidgets.QVBoxLayout()

        self.label_buttons_layout = QtWidgets.QHBoxLayout()

        # Auto-label buttons (on the right side)
        self.autoLabelImgButton = QtWidgets.QPushButton("Auto-label img")
        self.autoLabelImgButton.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][PURPLE]}; 
        """)

        self.label_buttons_layout.addWidget(self.autoLabelImgButton)

        self.autoLabelAllButton = QtWidgets.QPushButton("Auto-label all")
        self.autoLabelAllButton.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][PURPLE]}; 
        """)

        self.label_buttons_layout.addWidget(self.autoLabelAllButton)

        self.right_layout.addLayout(self.label_buttons_layout)

        # List of checkboxes (labels) below auto-label buttons
        self.labelList = QtWidgets.QListWidget()
        _, list_labels = self.dataset_manager.get_dataset_labels()  # Retrieve the actual labels
        self.labelList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)

        # Iterate through the actual labels and create a checkbox for each one
        for label in list_labels:
            # Create a widget to hold both the checkbox and the label name
            widget = QtWidgets.QWidget()    
            widget.setStyleSheet(f"""
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                text-align: center;
            """)
            layout = QtWidgets.QHBoxLayout(widget)

            checkbox = QtWidgets.QCheckBox() # TODO add borders
            label_widget = QtWidgets.QLabel(label)

            layout.addWidget(checkbox)
            layout.addWidget(label_widget)

            layout.setAlignment(QtCore.Qt.AlignLeft)
            layout.setContentsMargins(self.ui_styles[PADDINGS][LABELS_LEFT], self.ui_styles[PADDINGS][LABELS_UP], 0, 0)

            # Add the custom widget (with checkbox and label) to the list
            item = QtWidgets.QListWidgetItem()
            self.labelList.addItem(item)
            self.labelList.setItemWidget(item, widget)

        self.labelList.setFixedSize(self.ui_styles[SIZES][LABEL_LIST][WIDTH], self.ui_styles[SIZES][LABEL_LIST][HEIGHT])

        self.right_layout.addWidget(self.labelList)

        # Confirm labeling button
        self.confirmLabelButton = QtWidgets.QPushButton("Confirm labeling")
        self.confirmLabelButton.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
        """)

        self.right_layout.addWidget(self.confirmLabelButton)

        self.main_layout.addLayout(self.right_layout, 1, 2, 1, 1)

    def setup_dropdown_menu(self):
        # Long vertical button on the left (opens image grid)
        self.openImageGridButton = QtWidgets.QPushButton("Images")
        self.openImageGridButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.openImageGridButton.setFixedSize(self.ui_styles[SIZES][DROPDOWN_BUTTON][WIDTH], self.ui_styles[SIZES][DROPDOWN_BUTTON][HEIGHT])
        
        self.main_layout.addWidget(self.openImageGridButton, 1, 0, 1, 1)


        self.dropdown_layout = QtWidgets.QHBoxLayout()
        self.dropdown_layout.setContentsMargins(0, 0, 0, 0)
        self.dropdown_layout.setSpacing(0)

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
            font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]}; /* Outer border */
        """)

        # Create the layout for the scroll widget
        hidden_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        hidden_layout.setContentsMargins(self.ui_styles[PADDINGS][MIN_SIDES], self.ui_styles[PADDINGS][MIN_SIDES], self.ui_styles[PADDINGS][MIN_SIDES], self.ui_styles[PADDINGS][MIN_SIDES])

        # Add the button inside the layout
        self.importButton = QtWidgets.QPushButton("Import dataset images")
        self.importButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            padding: 3px;
        """)
        hidden_layout.addWidget(self.importButton, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.imageGridWidget = QtWidgets.QWidget()
        self.imageGridWidget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        self.imageGridLayout = QtWidgets.QGridLayout(self.imageGridWidget)
        self.imageGridLayout.setContentsMargins(0, 0, 0, 0)  # No margins for the grid layout
        self.imageGridLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        hidden_layout.addWidget(self.imageGridWidget)

        self.dropdown_layout.addWidget(self.scroll_widget)

        self.imageGridWidget.setStyleSheet("""
            QWidget {
                border: none;
            }
        """)

        self.closeImageGridButton = QtWidgets.QPushButton("Images")
        self.closeImageGridButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.closeImageGridButton.setFixedSize(self.ui_styles[SIZES][DROPDOWN_BUTTON][WIDTH], self.ui_styles[SIZES][DROPDOWN_BUTTON][HEIGHT])
        

        self.scroll_widget.setHidden(True)
        self.closeImageGridButton.setHidden(True)

        self.dropdown_layout.addWidget(self.closeImageGridButton, alignment=QtCore.Qt.AlignLeft)

        self.main_layout.addLayout(self.dropdown_layout, 1, 0, 1, 2)

    def populate_grid(self, label, label_idx):
        label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
        """)
        self.imageGridLayout.addWidget(label, label_idx // self.ui_styles[NUM_IMAGES_LABELING_GRID], label_idx % self.ui_styles[NUM_IMAGES_LABELING_GRID])