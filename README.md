
Built by https://www.blackbox.ai

---

# PDF Compression Tool

## Project Overview

The PDF Compression Tool is a web-based application designed to help users compress PDF files easily while preserving their quality. This tool features a user-friendly interface with drag-and-drop functionality, allowing users to upload and compress their files quickly. It showcases real-time feedback with progress indicators and provides a download option for the compressed files.

## Installation

To set up the PDF Compression Tool, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pdf-compressor.git
   cd pdf-compressor
   ```

2. **Set up a Python virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to `http://localhost:5000` to access the PDF Compression Tool.

3. **Upload your PDF file** by dragging it into the designated area or clicking to select it.

4. **Monitor the compression process** via the progress bar. Once completed, you will have the option to download your compressed PDF.

## Features

- Modern and responsive user interface developed with **Tailwind CSS**.
- **Drag & drop file upload** mechanism for convenient file selection.
- **Progress bar** to display the compression status in real-time.
- **Comparison display** for original and compressed PDF sizes.
- **Error messages** to assist with any issues during upload or compression.
- **Download button** for easy retrieval of compressed files.

## Dependencies

This project requires the following Python packages, as specified in `requirements.txt`:

- `Flask==2.0.1`: A web framework for building the server-side application.
- `PyPDF2==3.0.1`: A library for manipulating PDF files.
- `pikepdf==8.7.1`: A PDF manipulation library for advanced compression functionalities.

## Project Structure

The project is organized as follows:

```
pdf-compressor/
├── static/
│   ├── css/
│   │   └── style.css    # CSS styles for the user interface
│   └── js/
│       └── main.js      # JavaScript for frontend functionality
├── templates/
│   └── index.html       # Main HTML template for the application
├── app.py               # Flask application setup
├── compressor.py        # Compression logic and algorithms
└── requirements.txt     # Dependency list for the project
```

## Conclusion

The PDF Compression Tool is a simple yet powerful utility designed for handling PDF files efficiently. With its user-friendly interface and robust backend, it aims to provide an optimal experience for users looking to reduce their PDF file sizes without sacrificing quality. If you encounter any issues or have suggestions, feel free to contribute or raise concerns through appropriate channels.