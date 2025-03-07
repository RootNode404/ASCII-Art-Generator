from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QCheckBox, QSpinBox, QComboBox, QLineEdit, QMessageBox, QSystemTrayIcon
)
from PyQt6 import QtGui
import ascii_magic as am
import os, webbrowser, sys

class AsciiArtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.file = None
        self.ImgFile = None
        self.fromClipboard = False
        self.autoOpen = False


    def initUI(self):
        self.setWindowTitle("Ascii Art Generator")
        self.setWindowIcon(QtGui.QIcon("./assets/icon.png"))
        self.setGeometry(100, 100, 300, 280)

        layout = QVBoxLayout()

        self.color_options_label = QLabel("Color:")
        self.color_options = QComboBox()
        self.color_options.addItems(["Black & White", "RGB"])
        self.color_options.setCurrentIndex(1)

        self.auto_open_checkbox = QCheckBox("Auto Open:")
        self.auto_open_checkbox.stateChanged.connect(self.autoOpenToggle)

        self.print_location_label = QLabel("Print location:")
        self.print_location_options = QComboBox()
        self.print_location_options.addItems(["Terminal", "HTML File"])
        self.print_location_options.currentIndexChanged.connect(self.printComboBox)
        self.print_location_options.setCurrentIndex(1)

        self.resolution_spinbox_label = QLabel("Resolution:")
        self.resolution_spinbox = QSpinBox()
        self.resolution_spinbox.setRange(50, 10000)
        self.resolution_spinbox.setSingleStep(50)
        self.resolution_spinbox.setValue(100)

        self.custom_chars_entry_checkbox = QCheckBox("Custom Characters:")
        self.custom_chars_entry_checkbox.stateChanged.connect(self.customCharToggle)
        self.custom_chars_entry = QLineEdit()
        self.custom_chars_entry.setEnabled(False)

        self.image_from_clipboard_checkbox = QCheckBox("From Clipboard:")
        self.image_from_clipboard_checkbox.stateChanged.connect(self.fromClipboardToggle)



        self.open_file_button = QPushButton("Open File")
        self.open_file_button.clicked.connect(self.openFromFile)

        self.file_path_entry = QLineEdit()
        self.file_path_entry.setText("path/to/image/file")
        self.file_path_entry.setReadOnly(True)

        self.start_button = QPushButton("Generate")
        self.start_button.clicked.connect(self.start)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # Set the layout
        layout.addWidget(self.color_options_label)
        layout.addWidget(self.color_options)
        layout.addWidget(self.print_location_label)
        layout.addWidget(self.print_location_options)
        layout.addWidget(self.resolution_spinbox_label)
        layout.addWidget(self.resolution_spinbox)
        layout.addWidget(self.custom_chars_entry_checkbox)
        layout.addWidget(self.custom_chars_entry)
        layout.addWidget(self.image_from_clipboard_checkbox)
        layout.addWidget(self.auto_open_checkbox)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.file_path_entry)
        layout.addWidget(self.start_button)
        layout.addWidget(self.exit_button)

        # Push it to the gui
        self.setLayout(layout)

    # The main function
    def start(self):
        try:
            if self.fromClipboard:
                error = self.openFromClipboard()
                if error:
                    return
            elif not self.file:
                self.raiseError("Error", "Please open a file.")
                return

            # Handle the color
            if self.color_options.currentText() == "Black & White":
                monochrome = True
            elif self.color_options.currentText() == "RGB":
                monochrome = False

            print_location = self.print_location_options.currentText()
            art_resolution = self.resolution_spinbox.value()
            custom_chars = self.custom_chars_entry.text()
            filePath = "ascii-html.html"

            if print_location == "Terminal":
                self.ImgFile.to_terminal(columns=art_resolution, monochrome=monochrome, char=custom_chars)
            elif print_location == "HTML File":
                self.ImgFile.to_html_file(path="ascii-html.html", columns=art_resolution, monochrome=monochrome, char=custom_chars)

            if self.autoOpen:
                webbrowser.open(filePath)

            # Change the start button text to "Done"
            self.start_button.setText("Done")

        except Exception as e:
            self.raiseError("Error", str(e))

        self.start_button.setText("Generate")

    def customCharToggle(self, state):
        self.custom_chars_entry.setEnabled(state == 2)
        self.custom_chars_entry.clear()

    def fromClipboardToggle(self, state):
        self.fromClipboard = state == 2
        self.file_path_entry.setEnabled(not self.fromClipboard)
        self.open_file_button.setEnabled(not self.fromClipboard)

    def autoOpenToggle(self, state):
        self.autoOpen = state == 2

    def raiseError(self, title, message):
        QMessageBox.warning(self, title, message)

    def openFromFile(self):
        file_open, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg)")
        if file_open:
            self.file = file_open
            self.ImgFile = am.from_image(self.file)
            self.file_path_entry.setText(self.file)

    def openFromClipboard(self):
        try:
            self.ImgFile = am.from_clipboard()
        except:
            self.raiseError("Error", "No valid image was found in the clipboard")
            return True
        return False

    def printComboBox(self):
        val = self.print_location_options.currentText()
        if val == "Terminal":
            self.auto_open_checkbox.setChecked(False)
            self.auto_open_checkbox.setEnabled(False)
        else:
            self.auto_open_checkbox.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AsciiArtApp()
    window.show()
    sys.exit(app.exec())
