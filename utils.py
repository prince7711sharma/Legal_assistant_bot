
#from fpdf import FPDF

#def generate_pdf(question, answer):
#    pdf = FPDF()
#   pdf.add_page()
#   pdf.set_font("Arial", size=12)
#   pdf.multi_cell(0, 10, f"Question: {question}\n\nAnswer: {answer}")
#   filename = "legal_response.pdf"
#   pdf.output(filename)
#   return filename
from fpdf import FPDF
import os
import datetime


def generate_pdf(question, response, filename=None):
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"legal_response_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"Legal Question:\n{question}\n\nResponse:\n{response}")
    pdf.output(filename)

    return filename
