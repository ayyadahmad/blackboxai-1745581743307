from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from compressor import compress_pdf
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'pdf', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PDF or HTML file'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Generate output filename
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Get compression quality from request or use default
        quality_level = float(request.form.get('quality', 0.5))
        quality_level = max(0.1, min(0.9, quality_level))  # Ensure between 0.1 and 0.9
        
        # Compress PDF
        compression_result = compress_pdf(input_path, output_path, quality_level)
        
        # Clean up input file
        os.remove(input_path)
        
        # Send compressed file
        try:
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/pdf'
            )
        finally:
            # Clean up output file after sending
            if os.path.exists(output_path):
                os.remove(output_path)
    
    except Exception as e:
        # Clean up files in case of error
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
