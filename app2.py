import os
from fpdf import FPDF
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QCheckBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

# Define folder paths and default save folder
PDF_FOLDER = "SavedPDFs"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# Paths for image assets (update these with your file paths)
LOGO_ICON_PATH = os.path.join("images", "logo.png")
SETTINGS_ICON_PATH = os.path.join("images", "settings.png")
FILE_ICON_PATH = os.path.join("images", "folderbluer.png")

# Fonts folder path
FONTS_FOLDER = "fonts"
MINECRAFT_FONT_PATH = os.path.join(FONTS_FOLDER, "Minecraft.ttf")

# PDF class with Minecraft font
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Register the Minecraft font
        self.add_font("Minecraft", "", MINECRAFT_FONT_PATH, uni=True)

    def header(self):
        # Use Minecraft font for the header
        self.set_font("Minecraft", size=14)
        self.cell(0, 10, "Code to PDF Converter", border=0, ln=1, align="C")

    def add_code_content(self, content):
        self.set_font("Minecraft", size=12)
        for line in content.splitlines():
            self.multi_cell(0, 10, line)

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code to PDF Converter")
        self.setGeometry(100, 100, 600, 500)

        # Default settings
        self.is_drag_and_drop_enabled = True
        self.is_dark_mode = False
        self.save_folder = PDF_FOLDER
        self.file_path = None

        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Settings button at the top left
        settings_button = QPushButton(self)
        settings_button.setIcon(QIcon(SETTINGS_ICON_PATH))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.clicked.connect(self.open_settings_dialog)
        settings_button.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(settings_button, alignment=Qt.AlignLeft)

        # Logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(LOGO_ICON_PATH)
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title Label
        self.title_label = QLabel("Code to PDF Converter", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.title_label)

        # File selection
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText("Drag and drop a file here...")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px; background-color: #ecf0f1;")
        file_layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        file_layout.addWidget(browse_button)

        layout.addLayout(file_layout)

        # File type selection dropdown
        self.file_type_combobox = QComboBox(self)
        self.file_type_combobox.addItem("Text File (.txt)")
        self.file_type_combobox.addItem("Python File (.py)")
        self.file_type_combobox.addItem("Java File (.java)")
        self.file_type_combobox.addItem("C++ File (.cpp)")
        self.file_type_combobox.addItem("HTML File (.html)")
        self.file_type_combobox.addItem("CSS File (.css)")
        self.file_type_combobox.addItem("JavaScript File (.js)")
        self.file_type_combobox.addItem("Ruby File (.rb)")
        self.file_type_combobox.addItem("PHP File (.php)")
        self.file_type_combobox.addItem("Swift File (.swift)")
        self.file_type_combobox.addItem("Go File (.go)")
        self.file_type_combobox.addItem("Perl File (.pl)")
        self.file_type_combobox.addItem("TypeScript File (.ts)")
        self.file_type_combobox.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.file_type_combobox)

        # Convert Button
        convert_button = QPushButton("Convert to PDF", self)
        convert_button.clicked.connect(self.convert_to_pdf)
        convert_button.setStyleSheet("background-color: #2ecc71; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        layout.addWidget(convert_button)

        # Saved PDFs Section
        saved_label = QLabel("Saved PDFs", self)
        saved_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        layout.addWidget(saved_label)

        self.pdf_listbox = QListWidget(self)
        self.pdf_listbox.setStyleSheet("background-color: #ecf0f1; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.pdf_listbox.setIconSize(QSize(32, 32))  # Adjust icon size for list items
        layout.addWidget(self.pdf_listbox)

        # Buttons for managing PDFs
        button_layout = QHBoxLayout()

        delete_button = QPushButton("Delete Selected PDF", self)
        delete_button.clicked.connect(self.delete_pdf)
        delete_button.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(delete_button)

        open_folder_button = QPushButton("Open PDF Folder", self)
        open_folder_button.clicked.connect(self.open_pdf_folder)
        open_folder_button.setStyleSheet("background-color: #f39c12; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(open_folder_button)

        layout.addLayout(button_layout)

        # Set layout for the window
        self.setLayout(layout)

        # Refresh the list of PDFs on startup
        self.refresh_pdf_list()

        # Enable drag and drop (if implemented)
        self.setAcceptDrops(self.is_drag_and_drop_enabled)

        # Apply dark mode if enabled
        self.apply_dark_mode()

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(self.save_folder) if f.endswith(".pdf")]
        for pdf_file in pdf_files:
            item = QListWidgetItem(pdf_file)
            item.setIcon(QIcon(FILE_ICON_PATH))  # Set icon for the item
            self.pdf_listbox.addItem(item)

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path = file_path
            self.file_entry.setText(file_path)

    def convert_to_pdf(self):
        if not self.file_path:
            self.show_message("No File Selected", "Please select a file to convert.")
            return

        file_extension = os.path.splitext(self.file_path)[1]
        selected_type = self.file_type_combobox.currentText()
        valid_types = {
            "Text File (.txt)": ".txt",
            "Python File (.py)": ".py",
            "Java File (.java)": ".java",
            "C++ File (.cpp)": ".cpp",
            "HTML File (.html)": ".html",
            "CSS File (.css)": ".css",
            "JavaScript File (.js)": ".js",
            "Ruby File (.rb)": ".rb",
            "PHP File (.php)": ".php",
            "Swift File (.swift)": ".swift",
            "Go File (.go)": ".go",
            "Perl File (.pl)": ".pl",
            "TypeScript File (.ts)": ".ts"
        }

        if selected_type not in valid_types or file_extension != valid_types[selected_type]:
            self.show_message("Invalid File Type", "The selected file does not match the chosen type.")
            return

        try:
            pdf = PDF()
            pdf.add_page()
            with open(self.file_path, "r", encoding="utf-8") as file:
                pdf.add_code_content(file.read())

            pdf_filename = os.path.join(self.save_folder, os.path.basename(self.file_path).replace(file_extension, ".pdf"))
            pdf.output(pdf_filename)

            self.show_message("Success", f"PDF saved successfully: {pdf_filename}")
            self.refresh_pdf_list()
        except Exception as e:
            self.show_message("Error", f"An error occurred: {e}")

    def delete_pdf(self):
        current_item = self.pdf_listbox.currentItem()
        if current_item:
            pdf_file = os.path.join(self.save_folder, current_item.text())
            os.remove(pdf_file)
            self.refresh_pdf_list()

    def open_pdf_folder(self):
        os.startfile(self.save_folder)

    def open_settings_dialog(self):
        # Implement settings dialog as needed
        pass

    def apply_dark_mode(self):
        if self.is_dark_mode:
            self.setStyleSheet("background-color: #2C3E50; color: white;")
        else:
            self.setStyleSheet("background-color: #ecf0f1; color: black;")

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = App()
    main_window.show()
    sys.exit(app.exec_())
