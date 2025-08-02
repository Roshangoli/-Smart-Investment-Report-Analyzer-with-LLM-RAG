#!/usr/bin/env python3

"""
Utility script to convert the sample financial report text file to PDF format for testing.
"""

import os
import sys
from fpdf import FPDF

def create_pdf_from_text(input_file, output_file):
    """Convert a text file to PDF format."""
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False
        
        # Read the text file
        with open(input_file, 'r') as f:
            content = f.readlines()
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set font for title
        pdf.set_font("Arial", "B", 16)
        
        # Process content line by line
        for line in content:
            line = line.strip()
            
            # Handle headers
            if line.startswith('# '):
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, line[2:], ln=True)
            elif line.startswith('## '):
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, line[3:], ln=True)
            elif line.startswith('### '):
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, line[4:], ln=True)
            elif line.startswith('#### '):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 10, line[5:], ln=True)
            # Handle bullet points
            elif line.startswith('- '):
                pdf.set_font("Arial", "", 10)
                pdf.cell(10, 6, "•", ln=0)
                pdf.multi_cell(0, 6, line[2:])
            # Handle numbered lists
            elif line and line[0].isdigit() and line[1:].startswith('. '):
                pdf.set_font("Arial", "", 10)
                pdf.cell(10, 6, line.split('. ')[0] + ".", ln=0)
                pdf.multi_cell(0, 6, line.split('. ')[1])
            # Handle table headers
            elif line.startswith('|') and '-|-' in line:
                continue  # Skip table formatting lines
            # Handle table rows
            elif line.startswith('|'):
                pdf.set_font("Arial", "", 9)
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                cell_width = 190 / len(cells)
                for cell in cells:
                    pdf.cell(cell_width, 6, cell, border=1)
                pdf.ln()
            # Handle regular text
            elif line:
                pdf.set_font("Arial", "", 10)
                pdf.multi_cell(0, 6, line)
            # Handle empty lines
            else:
                pdf.ln(3)
        
        # Save the PDF
        pdf.output(output_file)
        print(f"PDF created successfully: {output_file}")
        return True
    
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        return False

def main():
    # Default file paths
    input_file = "sample_financial_report.txt"
    output_file = "sample_financial_report.pdf"
    
    # Check command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    # Create PDF
    success = create_pdf_from_text(input_file, output_file)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())