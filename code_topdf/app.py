import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from werkzeug.utils import secure_filename
from fpdf import FPDF

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret_key"

# Folders for uploads and PDFs
UPLOAD_FOLDER = 'uploads'
PDF_FOLDER = 'pdfs'

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.txt', '.py', '.java', '.cpp', '.html', '.css', '.js', '.rb', '.php', '.swift'}

# Configure folders in Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PDF_FOLDER'] = PDF_FOLDER


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Homepage with file upload."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and PDF generation."""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Generate PDF
        try:
            pdf_filename = generate_pdf(file_path, filename)
            flash(f'PDF generated: {pdf_filename}', 'success')
            return redirect(url_for('list_pdfs'))
        except Exception as e:
            flash(f'Error during PDF generation: {e}', 'error')
            return redirect(request.url)

    flash('Invalid file type', 'error')
    return redirect(request.url)


def generate_pdf(file_path, filename):
    """Convert code file to PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            pdf.multi_cell(0, 10, line)

    pdf_filename = os.path.splitext(filename)[0] + '.pdf'
    pdf.save_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
    pdf.output(pdf.save_path)
    return pdf_filename


@app.route('/pdfs')
def list_pdfs():
    """List all generated PDFs."""
    pdf_files = os.listdir(app.config['PDF_FOLDER'])
    return render_template('pdf_list.html', pdf_files=pdf_files)


@app.route('/pdfs/download/<filename>')
def download_pdf(filename):
    """Download a specific PDF."""
    return send_from_directory(app.config['PDF_FOLDER'], filename)


@app.route('/pdfs/delete/<filename>', methods=['POST'])
def delete_pdf(filename):
    """Delete a specific PDF."""
    file_path = os.path.join(app.config['PDF_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'{filename} deleted.', 'success')
    else:
        flash(f'{filename} not found.', 'error')
    return redirect(url_for('list_pdfs'))


@app.route('/settings')
def settings():
    """Settings page."""
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
