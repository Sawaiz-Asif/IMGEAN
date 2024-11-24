from PyQt5 import QtCore, QtGui, QtWidgets
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

class Ui_CheckImgQuality(object):
    def __init__(self, config, ui_styles):
        self.config = config
        self.ui_styles = ui_styles

    def setupUi(self, CheckImgQuality):
        CheckImgQuality.setObjectName("CheckImgQuality")
        
        self.centralwidget = QtWidgets.QWidget(CheckImgQuality)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout (Vertical Layout to hold all elements)
        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)

        # Title and Return Button (Top Section)
        self.setup_top_section()

        self.tab_selection_discarded = QPushButton("Discarded images")
        self.tab_selection_discarded.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][LIGHT_BLUE]}; 
        """)
        
        self.tab_selection_check = QPushButton("Images to check")
        self.tab_selection_check.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
        """)

        # Connect button clicks to the update function
        self.tab_selection_discarded.clicked.connect(lambda: self.set_active_tab(1))
        self.tab_selection_check.clicked.connect(lambda: self.set_active_tab(2))

        # Create the layout
        self.tab_selection_layout = QHBoxLayout()
        self.tab_selection_layout.addWidget(self.tab_selection_discarded, stretch=1)  # Initially, button 1 is bigger
        self.tab_selection_layout.addWidget(self.tab_selection_check, stretch=2)

        tab_selection_widget = QWidget()
        tab_selection_widget.setLayout(self.tab_selection_layout)

        # Add the QWidget (containing the layout) to the main layout
        self.main_layout.addWidget(tab_selection_widget, 1, 0)

        # Tab widget (for discarded images and images to check)
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setStyleSheet(f"""
            border: 0px;
            """)

        self.tabDiscarded = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tabDiscarded, "Discarded")

        self.tabToCheck = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tabToCheck, "Images to Check")

        self.tab_widget.setCurrentIndex(1)
        self.tab_widget.tabBar().hide()
        self.main_layout.addWidget(self.tab_widget, 2, 0)

        self.tab_components = {}
        self.tab_components["discarded"] = {}
        self.tab_components["checking"] = {}

        # ===================== Tab: Discarded Images ============================
        self.setupTab(self.tabDiscarded, "Delete", "Accept", "Reason: Automatic filtering (B&W)", "gridLayoutDiscarded")

        # ===================== Tab: Images to Check =============================
        self.setupTab(self.tabToCheck, "Discard", "Accept", None, "gridLayoutToCheck")

        # Set the central widget
        CheckImgQuality.setCentralWidget(self.centralwidget)
        self.retranslateUi(CheckImgQuality)
        QtCore.QMetaObject.connectSlotsByName(CheckImgQuality)

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
        self.main_layout.addLayout(self.top_section_layout, 0, 0)


    def setupTab(self, tab, first_button_text, second_button_text, reason_text, grid_layout_name):
        """Setup the layout for each tab with specified button text and reason label."""
        layout = QtWidgets.QHBoxLayout(tab)

        # Red Container (Left side, Image Grid and Button)
        left_container = QtWidgets.QWidget(tab)
        #red_container.setStyleSheet("background-color: lightcoral;")  # Red container
        left_layout = QtWidgets.QVBoxLayout(left_container)

        # Image Grid (in red container)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BACKGROUND]}; 
        """)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout(scroll_widget)
        grid_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        setattr(self, grid_layout_name, grid_layout)  # Dynamically set the layout as attribute
        scroll_area.setWidget(scroll_widget)

        left_layout.addWidget(scroll_area, 1)

        left_layout.addItem(QtWidgets.QSpacerItem(20, 58, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        if reason_text==None:
            current_components = self.tab_components["checking"]
            red_all_button = QtWidgets.QPushButton("Discard all")
        else:
            current_components = self.tab_components["discarded"]
            red_all_button = QtWidgets.QPushButton("Delete all")
    
        red_all_button.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
        """)
        self.allBtn = red_all_button
        current_components["red_all_button"] = red_all_button

        if reason_text==None:
            button_layout = QtWidgets.QHBoxLayout(left_container)

            accept_all = QtWidgets.QPushButton("Accept all")
            accept_all.setStyleSheet(f"""
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
            """)
            button_layout.addWidget(red_all_button)
            button_layout.addWidget(accept_all)
            left_layout.addLayout(button_layout)

            current_components["accept_all"] = accept_all
        else:
            left_layout.addWidget(red_all_button)

        layout.addWidget(left_container, 1)  # Add red container to tab layout

        # Yellow Container (Right side, Image Preview, Reason, and Navigation Buttons)
        right_container = QtWidgets.QWidget(tab)
        #yellow_container.setStyleSheet("background-color: lightyellow;")  # Yellow container
        right_layout = QtWidgets.QVBoxLayout(right_container)
        

        # Image Preview in yellow container
        image_preview = QtWidgets.QLabel()
        image_preview.setFixedSize(self.ui_styles[SIZES][IMG_PREVIEW][WIDTH], self.ui_styles[SIZES][IMG_PREVIEW][WIDTH])
        image_preview.setFrameShape(QtWidgets.QFrame.Box)
        image_preview.setAlignment(QtCore.Qt.AlignCenter)
        image_preview.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]+2}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BACKGROUND]}; 
        """)
        current_components["image_preview"] = image_preview
        right_layout.addWidget(image_preview)

        right_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Reason Label (in yellow container)
        if reason_text != None:
            self.reasonLabel = QtWidgets.QLabel(reason_text)

            regular_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][REGULAR_FONT_FILE])
            self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

            self.reasonLabel.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            text-align: center;
        """)
            self.reasonLabel.setAlignment(QtCore.Qt.AlignCenter)
            right_layout.addWidget(self.reasonLabel)

        # Add spacer to push the buttons down to the bottom
        right_layout.addItem(QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Navigation Buttons in yellow container (in a single row)
        nav_layout = QtWidgets.QHBoxLayout()
        prev_button = QtWidgets.QPushButton("Prev")
        prev_button.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
        """)
        self.prevBtn = prev_button
        current_components["prev_button"] = prev_button
        first_button = QtWidgets.QPushButton(first_button_text)  # First button (Discard or Delete)
        first_button.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
        """)
        self.firstBtn = first_button
        current_components["first_button"] = first_button
        second_button = QtWidgets.QPushButton(second_button_text)  # Second button (Always Accept)
        second_button.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
        """)
        self.secondBtn = second_button
        current_components["second_button"] = second_button
        next_button = QtWidgets.QPushButton("Next")
        next_button.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
        """)
        self.nextBtn = next_button
        current_components["next_button"] = next_button

        nav_layout.addWidget(self.prevBtn)
        nav_layout.addWidget(self.firstBtn)
        nav_layout.addWidget(self.secondBtn)
        nav_layout.addWidget(self.nextBtn)

        right_layout.addLayout(nav_layout)

        layout.addWidget(right_container, 1)  # Add yellow container to tab layout

    def retranslateUi(self, CheckImgQuality):
        _translate = QtCore.QCoreApplication.translate
        CheckImgQuality.setWindowTitle(_translate("CheckImgQuality", "Check Image Quality"))

    def set_active_tab(self, active_index):
        """
        Adjust button sizes and styles when a tab is selected.
        """
        if active_index == 1:
            # Make Button 1 larger
            self.tab_selection_layout.setStretch(0, 2)
            self.tab_selection_layout.setStretch(1, 1)
            self.update_button_styles(active_button=1)
            self.tab_widget.setCurrentIndex(0)
        elif active_index == 2:
            # Make Button 2 larger
            self.tab_selection_layout.setStretch(0, 1)
            self.tab_selection_layout.setStretch(1, 2)
            self.update_button_styles(active_button=2)
            self.tab_widget.setCurrentIndex(1)

    def update_button_styles(self, active_button):
        """
        Update the styles of the buttons to visually differentiate the active one.
        """
        if active_button == 1:
            self.tab_selection_check.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][LIGHT_BLUE]}; 
            """)
            self.tab_selection_discarded.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            """)
        elif active_button == 2:
            self.tab_selection_check.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            """)
            self.tab_selection_discarded.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][LIGHT_BLUE]}; 
            """)