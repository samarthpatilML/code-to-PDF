import os
from fpdf import FPDF
from tkinter import Tk, filedialog, messagebox, Button, Label, Listbox, END

# Folder to store generated PDFs
PDF_FOLDER = "SavedPDFs"

# Create the folder if it doesn't exist
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Text to PDF Conversion", 0, 1, "C")

# Function to convert text file to PDF
def convert_to_pdf():
    # Open file dialog for selecting a text file
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    
    # Check if a file was selected
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a text file to convert.")
        return

    # Ensure the selected file is a text file
    if not file_path.endswith(".txt"):
        messagebox.showerror("Invalid File", "Please select a valid text file (*.txt).")
        return

    try:
        # Initialize PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Read the content of the text file and write it to the PDF
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                pdf.multi_cell(0, 10, line)

        # Save the PDF to the SavedPDFs folder
        pdf_filename = os.path.join(PDF_FOLDER, os.path.basename(file_path).replace(".txt", ".pdf"))
        pdf.output(pdf_filename)

        # Notify the user of success and refresh the list
        messagebox.showinfo("Success", f"PDF saved successfully: {pdf_filename}")
        refresh_pdf_list()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the file: {e}")

# Function to refresh the list of stored PDFs
def refresh_pdf_list():
    pdf_listbox.delete(0, END)
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    for pdf in pdf_files:
        pdf_listbox.insert(END, pdf)

# Function to delete a selected PDF
def delete_pdf():
    selected = pdf_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a PDF to delete.")
        return

    pdf_name = pdf_listbox.get(selected)
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)
    try:
        os.remove(pdf_path)
        messagebox.showinfo("Success", f"Deleted: {pdf_name}")
        refresh_pdf_list()
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete {pdf_name}: {e}")

# Function to open the folder where PDFs are stored
def open_pdf_folder():
    os.startfile(PDF_FOLDER)

# GUI Application
def create_gui():
    root = Tk()
    root.title("Text to PDF Converter")
    root.geometry("500x400")

    # Title Label
    title_label = Label(root, text="Text to PDF Converter", font=("Arial", 16))
    title_label.pack(pady=10)

    # Convert Button
    convert_button = Button(root, text="Convert Text File to PDF", font=("Arial", 12), command=convert_to_pdf)
    convert_button.pack(pady=10)

    # Label for Saved PDFs
    saved_label = Label(root, text="Saved PDFs", font=("Arial", 14))
    saved_label.pack(pady=5)

    # Listbox to display stored PDFs
    global pdf_listbox
    pdf_listbox = Listbox(root, font=("Arial", 12), height=10, width=50)
    pdf_listbox.pack(pady=10)

    # Buttons for managing PDFs
    delete_button = Button(root, text="Delete Selected PDF", font=("Arial", 12), command=delete_pdf)
    delete_button.pack(pady=5)

    open_folder_button = Button(root, text="Open PDF Folder", font=("Arial", 12), command=open_pdf_folder)
    open_folder_button.pack(pady=5)

    # Refresh the list of PDFs on startup
    refresh_pdf_list()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
