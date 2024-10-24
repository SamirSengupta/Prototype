import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Function to modify the PDF
def modify_pdf_with_hidden_text(input_pdf_path, output_pdf_path, text_to_hide):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Copy all pages from the original PDF
    for page in reader.pages:
        writer.add_page(page)

    # Create a new PDF to hold the hidden text
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    c.setFont("Helvetica", 2)
    c.setFillColorRGB(1, 1, 1)

    # Split the input text into lines
    text_lines = text_to_hide.splitlines()

    # Starting position on the PDF (X, Y)
    x_position = 100
    y_position = 750

    for line in text_lines:
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 2)
            c.setFillColorRGB(1, 1, 1)
            y_position = 750
        c.drawString(x_position, y_position, line)
        y_position -= 5

    c.save()

    # Add the temporary PDF with hidden text as a new page
    with open(temp_pdf_path, "rb") as temp_pdf_file:
        hidden_text_reader = PdfReader(temp_pdf_file)
        writer.add_page(hidden_text_reader.pages[0])

    with open(output_pdf_path, "wb") as output_pdf_file:
        writer.write(output_pdf_file)

    os.remove(temp_pdf_path)

# Streamlit app
def main():
    st.title("PDF Modifier with Hidden Text")

    # File uploader for the input PDF
    input_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Text area to input the hidden text
    text_to_hide = st.text_area("Enter the text to hide in the PDF")

    if input_pdf and text_to_hide:
        # Save the uploaded PDF to a temporary file
        input_pdf_path = "uploaded_pdf.pdf"
        with open(input_pdf_path, "wb") as f:
            f.write(input_pdf.read())

        output_pdf_path = "output.pdf"

        # Modify the PDF
        modify_pdf_with_hidden_text(input_pdf_path, output_pdf_path, text_to_hide)

        # Provide a download link for the modified PDF
        with open(output_pdf_path, "rb") as f:
            st.download_button("Download modified PDF", f, file_name="output.pdf")

        # Cleanup the temporary files
        os.remove(input_pdf_path)
        os.remove(output_pdf_path)

if __name__ == "__main__":
    main()
