import re
import os
from pypdf import PdfReader
from docx import Document

class Inputter:
    def __init__(self, filename):
        self.filename = filename

    def clean_text(self, text):
        page_number_pattern = re.compile(r"^\s*\d+\s*$|^\s*Page\s+\d+\s*$", re.IGNORECASE)
        header_pattern = re.compile(r"(header text|document title|chapter \d+|any known pattern)", re.IGNORECASE)
        footer_pattern = re.compile(r"(footer text|confidential|any pattern you know)", re.IGNORECASE)

        lines = text.splitlines()

        clean_lines = [
            line for line in lines 
            if line.strip() and 
            not page_number_pattern.match(line.strip()) and 
            not header_pattern.match(line.strip()) and 
            not footer_pattern.match(line.strip())
        ]

        return "\n".join(line for line in clean_lines if line.strip())

    def read_pdf(self):
        try:
            reader = PdfReader(self.filename)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    clean_text = self.clean_text(text)
                    print(clean_text)
                    print("-" * 20, "\n")
        except Exception as e:
            print(f"Error reading PDF file: {e}")

    def read_docx(self):
        try:
            doc = Document(self.filename)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            clean_text = self.clean_text("\n".join(full_text))
            print(clean_text)
        except Exception as e:
            print(f"Error reading DOCX file: {e}")

    def read(self):
        file_ext = os.path.splitext(self.filename)[1].lower()

        if file_ext == ".pdf":
            self.read_pdf()
        elif file_ext == ".docx":
            self.read_docx()
        else:
            print("Unsupported file format. Please provide a PDF or DOCX file.")

def main():
    inputter = Inputter('datafiles/jeff101.pdf')  
    inputter.read()

if __name__ == "__main__":
    main()
