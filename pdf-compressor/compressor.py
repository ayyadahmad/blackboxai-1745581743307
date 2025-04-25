import os
import subprocess
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import re

def compress_pdf(input_path, output_path, quality_level=0.5):
    """Compress PDF file using aggressive settings"""
    try:
        if input_path.lower().endswith(".pdf"):
            # Create temporary files
            temp_dir = tempfile.mkdtemp()
            temp_output = os.path.join(temp_dir, "temp.pdf")
            
            # Aggressive Ghostscript compression
            subprocess.run([
                "gs", "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/screen",
                "-dNOPAUSE", "-dQUIET", "-dBATCH",
                "-dDownsampleColorImages=true",
                "-dColorImageResolution=50",
                "-dDownsampleGrayImages=true",
                "-dGrayImageResolution=50",
                "-dDownsampleMonoImages=true",
                "-dMonoImageResolution=50",
                "-dEmbedAllFonts=false",
                "-dSubsetFonts=true",
                "-dCompressFonts=true",
                f"-sOutputFile={temp_output}",
                input_path
            ], check=True)
            
            # QPDF optimization
            subprocess.run([
                "qpdf",
                "--object-streams=generate",
                "--compress-streams=y",
                "--compression-level=9",
                "--recompress-flate",
                "--optimize-images",
                temp_output,
                output_path
            ], check=True)
            
            # Clean up temp files
            if os.path.exists(temp_output):
                os.remove(temp_output)
            os.rmdir(temp_dir)
            
        elif input_path.lower().endswith(".html"):
            # Convert HTML to PDF first
            temp_pdf = output_path + ".temp.pdf"
            c = canvas.Canvas(temp_pdf, pagesize=A4)
            width, height = A4
            
            with open(input_path, "r") as html_file:
                content = html_file.read()
                
                # Process text content
                text = content.replace("<", " <").replace(">", "> ")
                text = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)
                text = re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)
                text = re.sub(r"<[^>]+>", " ", text)
                
                # Write text with minimal settings
                y = height - 30
                font_size = 6  # Very small font
                line_spacing = font_size
                c.setFont("Helvetica", font_size)
                
                for line in text.split("\n"):
                    if line.strip():
                        if y < 30:
                            c.showPage()
                            y = height - 30
                            c.setFont("Helvetica", font_size)
                        
                        words = line.split()
                        line_buffer = []
                        for word in words:
                            line_buffer.append(word)
                            test_line = " ".join(line_buffer)
                            if c.stringWidth(test_line) > width - 40:
                                c.drawString(20, y, " ".join(line_buffer[:-1]))
                                y -= line_spacing
                                line_buffer = [word]
                        
                        if line_buffer:
                            c.drawString(20, y, " ".join(line_buffer))
                            y -= line_spacing
            
            c.save()
            
            # Then compress the PDF
            compress_pdf(temp_pdf, output_path, quality_level)
            
            # Clean up temp file
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
        
        else:
            raise Exception("Unsupported file format")
        
        # Get compression statistics
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        return {
            "success": True,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio
        }
        
    except Exception as e:
        raise Exception(f"Error during PDF compression: {str(e)}")

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)
