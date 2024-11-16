import os
from fpdf import FPDF
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QListWidget, QMessageBox, QComboBox, QRadioButton, QCheckBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt

# Folder to store generated PDFs (default folder)
PDF_FOLDER = "SavedPDFs"

# Create the folder if it doesn't exist
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Code to PDF Conversion", 0, 1, "C")

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Code to PDF Converter")
        self.setGeometry(100, 100, 600, 450)

        # Default settings
        self.is_drag_and_drop_enabled = True
        self.is_dark_mode = False
        self.save_folder = PDF_FOLDER

        self.file_path = None
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

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

        # Add the settings menu button
        self.create_settings_menu()

        # Enable drag and drop
        self.setAcceptDrops(self.is_drag_and_drop_enabled)

    def create_settings_menu(self):
        # Create the settings button
        self.settings_button = QPushButton("☰", self)
        self.settings_button.setStyleSheet("font-size: 20px; background-color: transparent; border: none;")
        self.settings_button.clicked.connect(self.open_settings_dialog)

        # Add the settings button to the window
        self.settings_button.setGeometry(10, 10, 40, 40)  # Position it in the top left corner

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def toggle_drag_and_drop(self, enabled):
        self.is_drag_and_drop_enabled = enabled
        self.setAcceptDrops(self.is_drag_and_drop_enabled)

    def toggle_dark_mode(self, dark_mode):
        self.is_dark_mode = dark_mode
        if self.is_dark_mode:
            self.setStyleSheet("background-color: #2C3E50; color: white;")
        else:
            self.setStyleSheet("background-color: #ecf0f1; color: black;")

    def dragEnterEvent(self, event):
        if self.is_drag_and_drop_enabled and event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.is_drag_and_drop_enabled:
            file_url = event.mimeData().urls()[0].toLocalFile()
            self.file_path = file_url
            self.file_entry.setText(file_url)

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.List)

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
            "Swift File (.swift)": ".swift"
        }

        if selected_type not in valid_types or file_extension != valid_types[selected_type]:
            self.show_message("Invalid File Type", "The selected file does not match the chosen type.")
            return

        try:
            # Initialize PDF
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Read the content of the text file and write it to the PDF
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    pdf.multi_cell(0, 10, line)

            # Save the PDF in the chosen folder
            pdf_filename = os.path.join(self.save_folder, os.path.basename(self.file_path).replace(file_extension, ".pdf"))
            pdf.output(pdf_filename)

            self.show_message("Success", f"PDF saved successfully: {pdf_filename}")
            self.refresh_pdf_list()
        except Exception as e:
            self.show_message("Error", f"An error occurred while processing the file: {e}")

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(self.save_folder) if f.endswith(".pdf")]
        self.pdf_listbox.addItems(pdf_files)

    def delete_pdf(self):
        selected = self.pdf_listbox.selectedItems()
        if not selected:
            self.show_message("Warning", "Please select a PDF to delete.")
            return

        pdf_name = selected[0].text()
        pdf_path = os.path.join(self.save_folder, pdf_name)
        try:
            os.remove(pdf_path)
            self.show_message("Success", f"Deleted: {pdf_name}")
            self.refresh_pdf_list()
        except Exception as e:
            self.show_message("Error", f"Could not delete {pdf_name}: {e}")

    def open_pdf_folder(self):
        os.startfile(self.save_folder)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Dark Mode Radio Buttons
        dark_mode_label = QLabel("Dark Mode", self)
        self.dark_mode_radio = QRadioButton("Enable", self)
        self.light_mode_radio = QRadioButton("Disable", self)
        if parent.is_dark_mode:
            self.dark_mode_radio.setChecked(True)
        else:
            self.light_mode_radio.setChecked(True)

        layout.addWidget(dark_mode_label)
        layout.addWidget(self.dark_mode_radio)
        layout.addWidget(self.light_mode_radio)

        # Drag and Drop Checkbox
        self.drag_and_drop_checkbox = QCheckBox("Enable Drag and Drop", self)
        self.drag_and_drop_checkbox.setChecked(parent.is_drag_and_drop_enabled)
        layout.addWidget(self.drag_and_drop_checkbox)

        # Save Location Button
        self.save_location_button = QPushButton("Select Save Folder", self)
        self.save_location_button.clicked.connect(self.select_save_folder)
        layout.addWidget(self.save_location_button)

        # Buttons to apply settings
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.apply_settings)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def apply_settings(self):
        dark_mode = self.dark_mode_radio.isChecked()
        drag_and_drop = self.drag_and_drop_checkbox.isChecked()

        # Apply settings to the main app
        self.parent().toggle_dark_mode(dark_mode)
        self.parent().toggle_drag_and_drop(drag_and_drop)

        # Close the dialog
        self.accept()

    def select_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.parent().save_folder)
        if folder:
            self.parent().set_save_folder(folder)

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
