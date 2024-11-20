import os
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox, QComboBox, QCheckBox, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize

# Define folder paths and default save folder
PDF_FOLDER = "SavedPDFs"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# Paths for image assets (update these with your file paths)
LOGO_ICON_PATH = "logo.png"  # Path to the app's logo
SETTINGS_ICON_PATH = "settings.png"  # Path to the settings button icon
FILE_ICON_PATH = "folderbluer.png"  # Icon for each saved file in the list

# Define font path for a custom font
CUSTOM_FONT_PATH = "Minecraft.ttf"  # Path to your Minecraft font file


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Code to PDF Converter", 0, 1, "C")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code to PDF Converter")
        self.setGeometry(100, 100, 600, 500)

        # Default settings
        self.is_drag_and_drop_enabled = True
        self.save_folder = PDF_FOLDER
        self.file_path = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel(self)
        if os.path.exists(LOGO_ICON_PATH):
            logo_pixmap = QPixmap(LOGO_ICON_PATH)
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title Label
        title_label = QLabel("Code to PDF Converter", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title_label)

        # File selection
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText("Drag and drop a file here...")
        self.file_entry.setReadOnly(True)
        file_layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("background-color: #3498db; color: white; font-size: 14px;")
        file_layout.addWidget(browse_button)

        layout.addLayout(file_layout)

        # File type selection dropdown
        self.file_type_combobox = QComboBox(self)
        self.file_type_combobox.addItems([
            "Text File (.txt)", "Python File (.py)", "Java File (.java)",
            "C++ File (.cpp)", "HTML File (.html)", "CSS File (.css)",
            "JavaScript File (.js)", "Ruby File (.rb)", "PHP File (.php)",
            "Swift File (.swift)", "Go File (.go)", "Perl File (.pl)", "TypeScript File (.ts)"
        ])
        layout.addWidget(self.file_type_combobox)

        # Convert Button
        convert_button = QPushButton("Convert to PDF", self)
        convert_button.clicked.connect(self.convert_to_pdf)
        convert_button.setStyleSheet("background-color: #2ecc71; color: white; font-size: 14px;")
        layout.addWidget(convert_button)

        # Saved PDFs Section
        saved_label = QLabel("Saved PDFs", self)
        saved_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #AE445A;")
        layout.addWidget(saved_label)

        self.pdf_listbox = QListWidget(self)
        self.pdf_listbox.setStyleSheet("background-color: #ecf0f1; font-size: 14px;")
        layout.addWidget(self.pdf_listbox)

        # Buttons for managing PDFs
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete Selected PDF", self)
        delete_button.clicked.connect(self.delete_pdf)
        delete_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px;")
        button_layout.addWidget(delete_button)

        open_folder_button = QPushButton("Open PDF Folder", self)
        open_folder_button.clicked.connect(self.open_pdf_folder)
        open_folder_button.setStyleSheet("background-color: #f39c12; color: white; font-size: 14px;")
        button_layout.addWidget(open_folder_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Refresh the list of PDFs on startup
        self.refresh_pdf_list()

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(self.save_folder) if f.endswith(".pdf")]
        for pdf_file in pdf_files:
            item = QListWidgetItem(pdf_file)
            item.setIcon(QIcon(FILE_ICON_PATH))
            self.pdf_listbox.addItem(item)

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select a File", "", "All Files (*.*)")
        if file_path:
            self.file_path = file_path
            self.file_entry.setText(file_path)

    def convert_to_pdf(self):
        if not self.file_path:
            self.show_message("No File Selected", "Please select a file to convert.")
            return

        file_extension = os.path.splitext(self.file_path)[1]
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        with open(self.file_path, "r") as file:
            content = file.read()
            pdf.multi_cell(0, 10, content)

        output_pdf = os.path.join(self.save_folder, os.path.basename(self.file_path).replace(file_extension, ".pdf"))
        pdf.output(output_pdf)
        self.show_message("Conversion Successful", f"PDF saved to: {output_pdf}")
        self.refresh_pdf_list()

    def delete_pdf(self):
        selected_items = self.pdf_listbox.selectedItems()
        if not selected_items:
            self.show_message("No PDF Selected", "Please select a PDF to delete.")
            return

        for item in selected_items:
            pdf_path = os.path.join(self.save_folder, item.text())
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        self.show_message("PDF Deleted", "The selected PDF(s) have been deleted.")
        self.refresh_pdf_list()

    def open_pdf_folder(self):
        os.startfile(self.save_folder)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app_instance = App()
    app_instance.show()
    sys.exit(app.exec_())
