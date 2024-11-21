from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
import os
from fpdf import FPDF

# Define folder paths and default save folder
PDF_FOLDER = "SavedPDFs"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

LOGO_ICON_PATH = "logo.png"
SETTINGS_ICON_PATH = "settings.png"
FILE_ICON_PATH = "folderbluer.png"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "", 0, 1, "C")

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code to PDF Converter")
        self.setGeometry(100, 100, 800, 600)  # Increased default size
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings Button
        settings_button = QPushButton()
        settings_button.setIcon(QIcon(SETTINGS_ICON_PATH))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.clicked.connect(self.open_settings_dialog)
        settings_button.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(settings_button, alignment=Qt.AlignLeft)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(LOGO_ICON_PATH)
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        self.title_label = QLabel("Code to PDF Converter")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.title_label)

        # File Selection
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Drag and drop a file here...")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("font-size: 16px; padding: 5px;")
        file_layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("font-size: 16px; padding: 10px;")
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        # File Type Dropdown
        self.file_type_combobox = QComboBox()
        self.file_type_combobox.addItems([
            "Text File (.txt)", "Python File (.py)", "Java File (.java)",
            "C++ File (.cpp)", "HTML File (.html)", "CSS File (.css)",
            "JavaScript File (.js)", "Ruby File (.rb)", "PHP File (.php)",
            "Swift File (.swift)", "Go File (.go)", "Perl File (.pl)", 
            "TypeScript File (.ts)"
        ])
        self.file_type_combobox.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.file_type_combobox)

        # Convert Button
        convert_button = QPushButton("Convert to PDF")
        convert_button.clicked.connect(self.convert_to_pdf)
        convert_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #2ecc71; color: white;")
        layout.addWidget(convert_button)

        # Saved PDFs Section
        saved_label = QLabel("Saved PDFs")
        saved_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #34495e;")
        layout.addWidget(saved_label)

        self.pdf_listbox = QListWidget()
        self.pdf_listbox.setStyleSheet("font-size: 14px; background-color: #ecf0f1; padding: 5px;")
        self.pdf_listbox.setIconSize(QSize(32, 32))
        layout.addWidget(self.pdf_listbox)

        # Action Buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete Selected PDF")
        delete_button.clicked.connect(self.delete_pdf)
        delete_button.setStyleSheet("font-size: 14px; background-color: #e74c3c; color: white; padding: 10px;")
        button_layout.addWidget(delete_button)

        open_folder_button = QPushButton("Open PDF Folder")
        open_folder_button.clicked.connect(self.open_pdf_folder)
        open_folder_button.setStyleSheet("font-size: 14px; background-color: #f39c12; color: white; padding: 10px;")
        button_layout.addWidget(open_folder_button)
        layout.addLayout(button_layout)

        # Full-screen Button
        fullscreen_button = QPushButton("Toggle Full Screen")
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        fullscreen_button.setStyleSheet("font-size: 14px; background-color: #34495e; color: white; padding: 10px;")
        layout.addWidget(fullscreen_button)

        self.setLayout(layout)
        self.refresh_pdf_list()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        for pdf in pdf_files:
            item = QListWidgetItem(pdf)
            item.setIcon(QIcon(FILE_ICON_PATH))
            self.pdf_listbox.addItem(item)

    def browse_file(self):
        file_dialog = QFileDialog(self)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_entry.setText(file_path)

    def convert_to_pdf(self):
        QMessageBox.information(self, "Convert", "Conversion functionality here!")

    def delete_pdf(self):
        QMessageBox.information(self, "Delete", "Delete functionality here!")

    def open_pdf_folder(self):
        QMessageBox.information(self, "Folder", "Open folder functionality here!")

    def open_settings_dialog(self):
        QMessageBox.information(self, "Settings", "Settings dialog here!")

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code to PDF Converter")
        self.setGeometry(100, 100, 800, 600)  # Increased default size
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings Button
        settings_button = QPushButton()
        settings_button.setIcon(QIcon(SETTINGS_ICON_PATH))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.clicked.connect(self.open_settings_dialog)
        settings_button.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(settings_button, alignment=Qt.AlignLeft)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(LOGO_ICON_PATH)
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        self.title_label = QLabel("Code to PDF Converter")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.title_label)

        # File Selection
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Drag and drop a file here...")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("font-size: 16px; padding: 5px;")
        file_layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("font-size: 16px; padding: 10px;")
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        # File Type Dropdown
        self.file_type_combobox = QComboBox()
        self.file_type_combobox.addItems([
            "Text File (.txt)", "Python File (.py)", "Java File (.java)",
            "C++ File (.cpp)", "HTML File (.html)", "CSS File (.css)",
            "JavaScript File (.js)", "Ruby File (.rb)", "PHP File (.php)",
            "Swift File (.swift)", "Go File (.go)", "Perl File (.pl)", 
            "TypeScript File (.ts)"
        ])
        self.file_type_combobox.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.file_type_combobox)

        # Convert Button
        convert_button = QPushButton("Convert to PDF")
        convert_button.clicked.connect(self.convert_to_pdf)
        convert_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #2ecc71; color: white;")
        layout.addWidget(convert_button)

        # Saved PDFs Section
        saved_label = QLabel("Saved PDFs")
        saved_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #34495e;")
        layout.addWidget(saved_label)

        self.pdf_listbox = QListWidget()
        self.pdf_listbox.setStyleSheet("font-size: 14px; background-color: #ecf0f1; padding: 5px;")
        self.pdf_listbox.setIconSize(QSize(32, 32))
        layout.addWidget(self.pdf_listbox)

        # Action Buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete Selected PDF")
        delete_button.clicked.connect(self.delete_pdf)
        delete_button.setStyleSheet("font-size: 14px; background-color: #e74c3c; color: white; padding: 10px;")
        button_layout.addWidget(delete_button)

        open_folder_button = QPushButton("Open PDF Folder")
        open_folder_button.clicked.connect(self.open_pdf_folder)
        open_folder_button.setStyleSheet("font-size: 14px; background-color: #f39c12; color: white; padding: 10px;")
        button_layout.addWidget(open_folder_button)
        layout.addLayout(button_layout)

        # Full-screen Button
        fullscreen_button = QPushButton("Toggle Full Screen")
        fullscreen_button.clicked.connect(self.toggle_fullscreen)
        fullscreen_button.setStyleSheet("font-size: 14px; background-color: #34495e; color: white; padding: 10px;")
        layout.addWidget(fullscreen_button)

        self.setLayout(layout)
        self.refresh_pdf_list()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        logger.info("Toggled full screen")

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        for pdf in pdf_files:
            item = QListWidgetItem(pdf)
            item.setIcon(QIcon(FILE_ICON_PATH))
            self.pdf_listbox.addItem(item)
        logger.info("Refreshed PDF list")

    def browse_file(self):
        file_dialog = QFileDialog(self)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_entry.setText(file_path)
            logger.info("Browsed file: " + file_path)

    def