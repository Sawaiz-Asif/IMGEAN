from PyQt5 import QtWidgets, QtCore

class Ui_CheckImgQuality(object):
    def setupUi(self, CheckImgQuality):
        CheckImgQuality.setObjectName("CheckImgQuality")
        CheckImgQuality.resize(1000, 700)  # Adjusted size
        
        self.centralwidget = QtWidgets.QWidget(CheckImgQuality)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout (Vertical Layout to hold all elements)
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title and Return Button (Top Section)
        self.top_layout = QtWidgets.QHBoxLayout()
        self.returnButton = QtWidgets.QPushButton("Return")
        self.titleLabel = QtWidgets.QLabel("Check img quality")
        font = self.titleLabel.font()
        font.setPointSize(18)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.top_layout.addWidget(self.returnButton)
        self.top_layout.addStretch(1)
        self.top_layout.addWidget(self.titleLabel)
        self.top_layout.addStretch(1)
        self.main_layout.addLayout(self.top_layout)

        # Tab widget (for discarded images and images to check)
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabDiscarded = QtWidgets.QWidget()
        self.tabToCheck = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tabDiscarded, "Discarded")
        self.tab_widget.addTab(self.tabToCheck, "Images to Check")
        self.main_layout.addWidget(self.tab_widget, 1)  # Stretch factor 1

        # ===================== Tab: Discarded Images ============================
        self.setupTab(self.tabDiscarded, "Delete", "Accept", "Reason: Automatic filtering (B&W)", "gridLayoutDiscarded")

        # ===================== Tab: Images to Check =============================
        self.setupTab(self.tabToCheck, "Discard", "Accept", "", "gridLayoutToCheck")

        # Set the central widget
        CheckImgQuality.setCentralWidget(self.centralwidget)
        self.retranslateUi(CheckImgQuality)
        QtCore.QMetaObject.connectSlotsByName(CheckImgQuality)

    def setupTab(self, tab, first_button_text, second_button_text, reason_text, grid_layout_name):
        """Setup the layout for each tab with specified button text and reason label."""
        layout = QtWidgets.QHBoxLayout(tab)

        # Red Container (Left side, Image Grid and Button)
        red_container = QtWidgets.QWidget(tab)
        #red_container.setStyleSheet("background-color: lightcoral;")  # Red container
        red_layout = QtWidgets.QVBoxLayout(red_container)

        # Image Grid (in red container)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout(scroll_widget)
        setattr(self, grid_layout_name, grid_layout)  # Dynamically set the layout as attribute
        scroll_area.setWidget(scroll_widget)

        red_layout.addWidget(scroll_area, 1)

        layout.addWidget(red_container, 1)  # Add red container to tab layout

        # Yellow Container (Right side, Image Preview, Reason, and Navigation Buttons)
        yellow_container = QtWidgets.QWidget(tab)
        #yellow_container.setStyleSheet("background-color: lightyellow;")  # Yellow container
        yellow_layout = QtWidgets.QVBoxLayout(yellow_container)
        
        # Image Preview in yellow container
        self.imagePreview = QtWidgets.QLabel()
        self.imagePreview.setFixedSize(400, 380)
        self.imagePreview.setFrameShape(QtWidgets.QFrame.Box)
        self.imagePreview.setAlignment(QtCore.Qt.AlignCenter)
        yellow_layout.addWidget(self.imagePreview)

        # Reason Label (in yellow container)
        self.reasonLabel = QtWidgets.QLabel(reason_text)
        self.reasonLabel.setAlignment(QtCore.Qt.AlignCenter)
        yellow_layout.addWidget(self.reasonLabel)

        # Add spacer to push the buttons down to the bottom
        yellow_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Navigation Buttons in yellow container (in a single row)
        nav_layout = QtWidgets.QHBoxLayout()
        self.prevBtn = QtWidgets.QPushButton("Prev")
        self.firstBtn = QtWidgets.QPushButton(first_button_text)  # First button (Discard or Delete)
        self.secondBtn = QtWidgets.QPushButton(second_button_text)  # Second button (Always Accept)
        self.nextBtn = QtWidgets.QPushButton("Next")

        nav_layout.addWidget(self.prevBtn)
        nav_layout.addWidget(self.firstBtn)
        nav_layout.addWidget(self.secondBtn)
        nav_layout.addWidget(self.nextBtn)

        yellow_layout.addLayout(nav_layout)

        layout.addWidget(yellow_container, 1)  # Add yellow container to tab layout

    def retranslateUi(self, CheckImgQuality):
        _translate = QtCore.QCoreApplication.translate
        CheckImgQuality.setWindowTitle(_translate("CheckImgQuality", "Check Image Quality"))