import zipfile
import io
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import cairosvg

def convert_svg_to_png(svg_data):
    """Converts SVG data to PNG format using cairosvg."""
    png_image = io.BytesIO()
    cairosvg.svg2png(bytestring=svg_data, write_to=png_image)
    return png_image.getvalue()

def create_pdf_from_images(image_data_list, output_pdf_path):
    """Creates a PDF from a list of image data."""
    if not image_data_list:
        print("No images to add to the PDF.")
        return

    c = canvas.Canvas(output_pdf_path)
    for image_data in image_data_list:
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size
        c.setPageSize((width, height))
        c.drawImage(io.BytesIO(image_data), 0, 0, width=width, height=height)
        c.showPage()
    c.save()

def main(zip_file_path, output_pdf_path):
    """Extracts SVG files from ZIP, converts them to PNG, and combines them into a PDF."""
    
    # Check if the ZIP file exists
    if not os.path.isfile(zip_file_path):
        print(f"File not found: {zip_file_path}")
        return

    image_data_list = []
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            if file_name.endswith('.svg'):
                svg_data = zip_file.read(file_name)
                png_data = convert_svg_to_png(svg_data)
                image_data_list.append(png_data)
    
    create_pdf_from_images(image_data_list, output_pdf_path)

if __name__ == '__main__':
    # Update these paths as needed
    zip_file_path = 'designs.zip'
    output_pdf_path = 'output.pdf'

    # Print the current working directory
    print(f"Current working directory: {os.getcwd()}")

    main(zip_file_path, output_pdf_path)
