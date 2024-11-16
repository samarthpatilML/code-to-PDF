import os
from fpdf import FPDF
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QListWidget, QMessageBox
from PyQt5.QtCore import Qt


# Folder to store generated PDFs
PDF_FOLDER = "SavedPDFs"

# Create the folder if it doesn't exist
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Text to PDF Conversion", 0, 1, "C")


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to PDF Converter")
        self.setGeometry(100, 100, 600, 450)

        self.file_path = None
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Text to PDF Converter", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(title_label)

        # File selection
        file_layout = QHBoxLayout()
        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText("Select a text file...")
        self.file_entry.setReadOnly(True)
        self.file_entry.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px; background-color: #ecf0f1;")
        file_layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("background-color: #3498db; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        file_layout.addWidget(browse_button)

        layout.addLayout(file_layout)

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

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Text Files (*.txt)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path = file_path
            self.file_entry.setText(file_path)

    def convert_to_pdf(self):
        if not self.file_path:
            self.show_message("No File Selected", "Please select a text file to convert.")
            return

        if not self.file_path.endswith(".txt"):
            self.show_message("Invalid File", "Please select a valid text file (*.txt).")
            return

        try:
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    pdf.multi_cell(0, 10, line)

            # Save the PDF in the SavedPDFs folder
            pdf_filename = os.path.join(PDF_FOLDER, os.path.basename(self.file_path).replace(".txt", ".pdf"))
            pdf.output(pdf_filename)

            self.show_message("Success", f"PDF saved successfully: {pdf_filename}")
            self.refresh_pdf_list()

        except Exception as e:
            self.show_message("Error", f"An error occurred while processing the file: {e}")

    def refresh_pdf_list(self):
        self.pdf_listbox.clear()
        pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        self.pdf_listbox.addItems(pdf_files)

    def delete_pdf(self):
        selected_item = self.pdf_listbox.currentItem()
        if not selected_item:
            self.show_message("Warning", "Please select a PDF to delete.")
            return

        pdf_name = selected_item.text()
        pdf_path = os.path.join(PDF_FOLDER, pdf_name)

        try:
            os.remove(pdf_path)
            self.show_message("Success", f"Deleted: {pdf_name}")
            self.refresh_pdf_list()

        except Exception as e:
            self.show_message("Error", f"Could not delete {pdf_name}: {e}")

    def open_pdf_folder(self):
        os.startfile(PDF_FOLDER)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
