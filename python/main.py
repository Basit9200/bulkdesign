import pandas as pd
import svgwrite
from fpdf import FPDF
import os

# Load and parse the Excel file
def read_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Generate SVG based on a template and row data
def generate_svg(row, svg_template_path='design.svg'):
    with open(svg_template_path, 'r') as file:
        svg_template = file.read()
    
    svg_content = svg_template
    for i in range(len(row)):
        # Use iloc for positional indexing
        svg_content = svg_content.replace(f'{{{{row.iloc[{i}]}}}}', str(row.iloc[i]) if pd.notna(row.iloc[i]) else '')
    
    svg_file = 'temp.svg'
    with open(svg_file, 'w') as file:
        file.write(svg_content)
    
    return svg_file

# Generate a PDF from SVG files
def generate_pdf(svg_files, pdf_file_path='document.pdf'):
    pdf = FPDF()
    
    for svg_file in svg_files:
        # Add each SVG as a new page (placeholder approach)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, txt=f"SVG file: {svg_file}", ln=True, align='C')
    
    pdf.output(pdf_file_path)

# Main function
def main(excel_file, svg_template_path='design.svg', output_pdf='document.pdf'):
    # Read the Excel file
    df = read_excel(excel_file)
    
    # Generate SVGs for each row
    svg_files = []
    for _, row in df.iterrows():
        svg_file = generate_svg(row, svg_template_path)
        svg_files.append(svg_file)
    
    # Generate PDF
    generate_pdf(svg_files, output_pdf)
    
    # Clean up temporary SVG files
    for svg_file in svg_files:
        if os.path.exists(svg_file):
            os.remove(svg_file)

if __name__ == "__main__":
    excel_file = 'input.xlsx'  # Path to your Excel file
    main(excel_file)
