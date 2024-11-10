from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_genrate_images(object):
    def setupUi(self, genrate_images, config):
        """Initialize the UI and load settings from the configuration file."""
        self.config = config  # Store the config for later use

        # Read colors from the config, use defaults if not found
        self.colors = self.config.get('UI_STYLES', {}).get('colors', {})
        self.default_colors = {
            'button_cancel': '#ff6666',
            'button_generate': '#66cc66',
            'progress_bar': '#00aaff',
            'background': '#f0f0f0'
        }

        # Set up main window properties
        genrate_images.setObjectName("genrate_images")
        genrate_images.resize(900, 650)
        
        # Set background color
        background_color = self.colors.get('background', self.default_colors['background'])
        genrate_images.setStyleSheet(f"background-color: {background_color};")

        self.centralwidget = QtWidgets.QWidget(genrate_images)
        self.centralwidget.setObjectName("centralwidget")
        self.main_grid = QtWidgets.QGridLayout(self.centralwidget)

        # Top Section - Return button and Title
        self.setup_top_section()

        # Left Section - Form controls
        self.setup_left_section()

        # Right Section - Image Preview and Progress Bar
        self.setup_right_section()

        # Bottom Section - Buttons
        self.setup_bottom_buttons()

        genrate_images.setCentralWidget(self.centralwidget)
        genrate_images.setWindowTitle("IMGEAN")

        self.load_models()  # Load models from configuration
        self.load_quality_checks()  # Load quality checks from configuration
        self.load_initial_values()  # Load initial values from config

    def setup_top_section(self):
        """Setup the top section with title and return button."""
        self.top_layout = QtWidgets.QHBoxLayout()
        self.return_button = QtWidgets.QPushButton("Return", self.centralwidget)
        self.top_layout.addWidget(self.return_button)

        self.label_title = QtWidgets.QLabel("Generate Images", self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.top_layout.addWidget(self.label_title)

        self.main_grid.addLayout(self.top_layout, 0, 0, 1, 2)

    def setup_left_section(self):
        """Setup the left section with form controls."""
        self.left_layout = QtWidgets.QFormLayout()

        # Prompt Input (Directly set text from config)
        self.label_prompt = QtWidgets.QLabel("Prompt:")
        self.text_prompt = QtWidgets.QTextEdit()
        self.text_prompt.setText(self.config['GENERATION']['PROMPTS'].get('positive', ''))
        self.left_layout.addRow(self.label_prompt, self.text_prompt)

        # Negative Prompt Input (Directly set text from config)
        self.label_negative_prompt = QtWidgets.QLabel("Negative Prompt:")
        self.text_negative_prompt = QtWidgets.QTextEdit()
        self.text_negative_prompt.setText(self.config['GENERATION']['PROMPTS'].get('negative', ''))
        self.left_layout.addRow(self.label_negative_prompt, self.text_negative_prompt)

        # Number of images
        self.label_images = QtWidgets.QLabel("Number of images:")
        self.spin_images = QtWidgets.QSpinBox()
        self.spin_images.setRange(1, 100)
        self.left_layout.addRow(self.label_images, self.spin_images)

        # Resolution
        self.label_resolution = QtWidgets.QLabel("Resolution:")
        self.spin_resolution_width = QtWidgets.QSpinBox()
        self.spin_resolution_width.setRange(256, 2048)
        self.spin_resolution_height = QtWidgets.QSpinBox()
        self.spin_resolution_height.setRange(256, 2048)

        res_layout = QtWidgets.QHBoxLayout()
        res_layout.addWidget(self.spin_resolution_width)
        res_layout.addWidget(QtWidgets.QLabel("X"))
        res_layout.addWidget(self.spin_resolution_height)
        self.left_layout.addRow(self.label_resolution, res_layout)

        # Model selection
        self.label_model = QtWidgets.QLabel("Model:")
        self.combo_model = QtWidgets.QComboBox()
        self.left_layout.addRow(self.label_model, self.combo_model)

        # Steps
        self.label_steps = QtWidgets.QLabel("Number of steps:")
        self.spin_steps = QtWidgets.QSpinBox()
        self.spin_steps.setRange(1, 50)
        self.left_layout.addRow(self.label_steps, self.spin_steps)

        # File Name and Seed
        self.label_filename = QtWidgets.QLabel("File Name:")
        self.text_filename = QtWidgets.QLineEdit()
        self.text_filename.setText(self.config['GENERATION'].get('filename', 'generated_image'))
        self.text_filename.setPlaceholderText("Enter filename")
        self.text_filename.editingFinished.connect(self.validate_filename)
        self.left_layout.addRow(self.label_filename, self.text_filename)

        self.label_seed = QtWidgets.QLabel("Seed :")
        self.text_seed = QtWidgets.QLineEdit()
        self.text_seed.setValidator(QtGui.QIntValidator())  # Ensure only integers are accepted
        self.text_seed.setPlaceholderText("Optional")  # Placeholder text
        self.left_layout.addRow(self.label_seed, self.text_seed)

        # Manual Quality Check
        self.checkbox_manual = QtWidgets.QCheckBox("Manual Quality Check")
        self.left_layout.addRow(self.checkbox_manual)

        # Quality Checks
        self.label_auto_check = QtWidgets.QLabel("Automatic Quality Check:")
        self.auto_check_list = QtWidgets.QListWidget()
        self.auto_check_list.setFixedHeight(100)
        self.left_layout.addRow(self.label_auto_check, self.auto_check_list)

        self.main_grid.addLayout(self.left_layout, 1, 0)

    def setup_right_section(self):
        """Setup the right section with image preview and progress bar."""
        self.right_layout = QtWidgets.QVBoxLayout()
        # Setup QGraphicsView with scene
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphics_view.setScene(QtWidgets.QGraphicsScene(self.graphics_view))
        self.graphics_view.setAlignment(QtCore.Qt.AlignCenter)
        self.right_layout.addWidget(self.graphics_view)
        # Setup a simple progress bar
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)  # Start at 0
        self.progress_bar.setTextVisible(True)  # Make the text visible
        self.right_layout.addWidget(self.progress_bar)

        self.main_grid.addLayout(self.right_layout, 1, 1)

    def setup_bottom_buttons(self):
        """Setup the bottom buttons (Cancel and Generate)."""
        self.button_layout = QtWidgets.QHBoxLayout()
        cancel_color = self.colors.get('button_cancel', self.default_colors['button_cancel'])
        self.cancel_button = QtWidgets.QPushButton("Cancel", self.centralwidget)
        self.cancel_button.setStyleSheet(f"background-color: {cancel_color}; color: white;")
        self.button_layout.addWidget(self.cancel_button)

        generate_color = self.colors.get('button_generate', self.default_colors['button_generate'])
        self.generate_button = QtWidgets.QPushButton("Generate", self.centralwidget)
        self.generate_button.setStyleSheet(f"background-color: {generate_color}; color: white;")
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
            item = QtWidgets.QListWidgetItem(func['name'])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.auto_check_list.addItem(item)

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