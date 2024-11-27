from PyQt5 import QtCore, QtGui, QtWidgets
class AddThresholdDialog(QtWidgets.QDialog):
    def __init__(self, min_value, max_value, color=None, value=None, parent=None):
        """
        Dialog for adding/editing a confidence threshold.
        If `color` and `value` are provided, the dialog works in edit mode.
        """
        super(AddThresholdDialog, self).__init__(parent)
        self.setWindowTitle("Edit Confidence Threshold" if color else "Add Confidence Threshold")
        self.setFixedSize(300, 150)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Color selection dropdown
        self.colorLabel = QtWidgets.QLabel("Select Color:")
        self.colorComboBox = QtWidgets.QComboBox()
        self.colorComboBox.addItems(["red", "green", "blue", "yellow", "orange", "purple"])
        if color:
            self.colorComboBox.setCurrentText(color)

        # Threshold value spin box
        self.thresholdLabel = QtWidgets.QLabel(f"Enter Threshold Value ({min_value} - {max_value}):")
        self.thresholdSpinBox = QtWidgets.QDoubleSpinBox()
        self.thresholdSpinBox.setMinimum(min_value)
        self.thresholdSpinBox.setMaximum(max_value)
        self.thresholdSpinBox.setSingleStep(0.01)
        self.thresholdSpinBox.setValue(value if value else min_value)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add widgets to layout
        self.layout.addWidget(self.colorLabel)
        self.layout.addWidget(self.colorComboBox)
        self.layout.addWidget(self.thresholdLabel)
        self.layout.addWidget(self.thresholdSpinBox)
        self.layout.addWidget(self.buttonBox)

    def get_data(self):
        """Return the selected color and threshold value."""
        return self.colorComboBox.currentText(), self.thresholdSpinBox.value()
