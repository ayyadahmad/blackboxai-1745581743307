import os
import subprocess
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from PIL import Image
import io
import re

def compress_pdf(input_path, output_path, quality_level=0.5):
    """Compress PDF file using multi-pass compression with Ghostscript and qpdf"""
    try:
        if input_path.lower().endswith(".pdf"):
            # Create temporary files
            temp_dir = tempfile.mkdtemp()
            temp1 = os.path.join(temp_dir, "1.pdf")
            temp2 = os.path.join(temp_dir, "2.pdf")
            
            # First pass: Extreme compression with Ghostscript
            subprocess.run([
                "gs",
                "-sDEVICE=pdfwrite",
                "-dNOPAUSE",
                "-dBATCH",
                "-dQUIET",
                "-dPDFSETTINGS=/screen",
                "-dCompatibilityLevel=1.4",
                "-dDownsampleColorImages=true",
                "-dDownsampleGrayImages=true",
                "-dDownsampleMonoImages=true",
                "-dColorImageResolution=10",
                "-dGrayImageResolution=10",
                "-dMonoImageResolution=10",
                "-dEmbedAllFonts=false",
                "-dSubsetFonts=true",
                "-dCompressFonts=true",
                f"-sOutputFile={temp1}",
                input_path
            ], check=True)
            
            # Second pass: Maximum compression with qpdf
            subprocess.run([
                "qpdf",
                "--object-streams=generate",
                "--compress-streams=y",
                "--compression-level=9",
                "--recompress-flate",
                "--optimize-images",
                "--linearize",
                temp1,
                temp2
            ], check=True)
            
            # Final pass: Additional Ghostscript optimization
            subprocess.run([
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/screen",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                "-dFastWebView=true",
                f"-sOutputFile={output_path}",
                temp2
            ], check=True)
            
            # Clean up temp files
            for f in [temp1, temp2]:
                if os.path.exists(f):
                    os.remove(f)
            os.rmdir(temp_dir)
            
        elif input_path.lower().endswith(".html"):
            # Convert HTML to PDF first with minimal settings
            temp_pdf = output_path + ".temp.pdf"
            page_width = 3 * inch
            page_height = 4 * inch
            c = canvas.Canvas(temp_pdf, pagesize=(page_width, page_height))
            
            with open(input_path, "r") as html_file:
                content = html_file.read()
                
                # Process text content
                text = content.replace("<", " ").replace(">", " ")
                text = re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)
                text = re.sub(r"<script>.*?</script>", "", text, flags=re.DOTALL)
                text = re.sub(r"<[^>]+>", " ", text)
                text = re.sub(r"\s+", " ", text).strip()
                
                y = page_height - 5
                font_size = 3
                line_spacing = font_size * 0.7
                c.setFont("Courier", font_size)
                
                words = text.split()
                line = []
                for word in words:
                    line.append(word)
                    if len("".join(line)) > 25:
                        if y < 5:
                            c.showPage()
                            y = page_height - 5
                            c.setFont("Courier", font_size)
                        c.drawString(3, y, "".join(line[:-1]))
                        y -= line_spacing
                        line = [word]
                
                if line:
                    if y < 5:
                        c.showPage()
                        y = page_height - 5
                        c.setFont("Courier", font_size)
                    c.drawString(3, y, "".join(line))
            
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
