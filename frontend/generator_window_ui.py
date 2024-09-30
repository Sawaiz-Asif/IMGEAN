from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_genrate_images(object):
    def setupUi(self, genrate_images):
        genrate_images.setObjectName("genrate_images")
        genrate_images.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(genrate_images)
        self.centralwidget.setObjectName("centralwidget")

        # Main Grid Layout to hold everything
        self.main_grid = QtWidgets.QGridLayout(self.centralwidget)

        # Top Section - Return button and Title
        self.top_layout = QtWidgets.QHBoxLayout()
        self.return_button = QtWidgets.QPushButton(self.centralwidget)
        self.return_button.setText("Return")
        self.return_button.setObjectName("return_button")
        self.top_layout.addWidget(self.return_button)

        self.label_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setText("Generate Images")
        self.top_layout.addWidget(self.label_title)

        # Add top layout to the main grid (First Row)
        self.main_grid.addLayout(self.top_layout, 0, 0, 1, 2)

        # Left Section - All form controls
        self.left_layout = QtWidgets.QFormLayout()

        # Prompt Input
        self.label_prompt = QtWidgets.QLabel("Prompt:")
        self.text_prompt = QtWidgets.QTextEdit()
        self.left_layout.addRow(self.label_prompt, self.text_prompt)

        # Number of images input
        self.label_images = QtWidgets.QLabel("Number of images:")
        self.combo_images = QtWidgets.QComboBox()
        self.combo_images.addItems([str(i) for i in range(1, 101)])  # Example range 1-100
        self.left_layout.addRow(self.label_images, self.combo_images)

        # Resolution input (two combo boxes for width and height)
        self.label_resolution = QtWidgets.QLabel("Resolution:")
        self.combo_resolution_width = QtWidgets.QComboBox()
        self.combo_resolution_width.addItems(["1024", "512", "256"])
        self.combo_resolution_height = QtWidgets.QComboBox()
        self.combo_resolution_height.addItems(["1024", "512", "256"])
        res_layout = QtWidgets.QHBoxLayout()
        res_layout.addWidget(self.combo_resolution_width)
        res_layout.addWidget(QtWidgets.QLabel("X"))
        res_layout.addWidget(self.combo_resolution_height)
        self.left_layout.addRow(self.label_resolution, res_layout)

        # Model selection
        self.label_model = QtWidgets.QLabel("Model:")
        self.combo_model = QtWidgets.QComboBox()
        self.combo_model.addItems(["StableDiffusion1", "StableDiffusion2", "StableDiffusion3"])
        self.left_layout.addRow(self.label_model, self.combo_model)

        # Number of steps input
        self.label_steps = QtWidgets.QLabel("Number of steps:")
        self.combo_steps = QtWidgets.QComboBox()
        self.combo_steps.addItems([str(i) for i in range(1, 11)])  # Example range 1-10
        self.left_layout.addRow(self.label_steps, self.combo_steps)

        # FileName and Seed Inputs
        self.label_filename = QtWidgets.QLabel("File Name:")
        self.text_filename = QtWidgets.QLineEdit()
        self.left_layout.addRow(self.label_filename, self.text_filename)

        self.label_seed = QtWidgets.QLabel("Seed:")
        self.text_seed = QtWidgets.QLineEdit()
        self.left_layout.addRow(self.label_seed, self.text_seed)

        # Manual Quality Check Checkbox
        self.checkbox_manual = QtWidgets.QCheckBox("Manual Quality Check")
        self.left_layout.addRow(self.checkbox_manual)

        # Automatic Quality Check List
        self.label_auto_check = QtWidgets.QLabel("Automatic Quality Check:")
        self.auto_check_list = QtWidgets.QListWidget()
        self.auto_check_list.addItems(["B&W", "Pose", "CustomChecker3"])
        self.left_layout.addRow(self.label_auto_check, self.auto_check_list)

        # Add left layout to the main grid (Left side)
        self.main_grid.addLayout(self.left_layout, 1, 0)

        # Right Section - Image Preview and Progress Bar
        self.right_layout = QtWidgets.QVBoxLayout()
        
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.right_layout.addWidget(self.graphics_view)
        
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setProperty("value", 48)
        self.right_layout.addWidget(self.progress_bar)

        # Add right layout to the main grid (Right side)
        self.main_grid.addLayout(self.right_layout, 1, 1)

        # Bottom Section - Cancel and Generate buttons
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setText("Cancel")
        self.bottom_layout.addWidget(self.cancel_button)

        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setText("Generate")
        self.bottom_layout.addWidget(self.generate_button)

        # Add bottom layout to the main grid (Last Row)
        self.main_grid.addLayout(self.bottom_layout, 2, 0, 1, 2)

        genrate_images.setCentralWidget(self.centralwidget)

        self.retranslateUi(genrate_images)
        QtCore.QMetaObject.connectSlotsByName(genrate_images)

    def retranslateUi(self, genrate_images):
        genrate_images.setWindowTitle("Generate Images")