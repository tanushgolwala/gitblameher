import re
from pypdf import PdfReader
from docx import Document

class Inputter:
    def __init__(self, input_source, flag):
        self.input_source = input_source
        self.flag = flag

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
            reader = PdfReader(self.input_source)
            full_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    clean_text = self.clean_text(text)
                    full_text.append(clean_text)
            return "\n".join(full_text)
        except Exception as e:
            return f"Error reading PDF file: {e}"

    def read_docx(self):
        try:
            doc = Document(self.input_source)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            clean_text = self.clean_text("\n".join(full_text))
            return clean_text
        except Exception as e:
            return f"Error reading DOCX file: {e}"

    def read_text(self):
        clean_text = self.clean_text(self.input_source)
        return clean_text

    def read(self):
        if self.flag == 1:
            return self.read_pdf()
        elif self.flag == 2:
            return self.read_docx()
        elif self.flag == 3:
            return self.read_text()
        else:
            return "Invalid input flag. Please use 1 (PDF), 2 (DOCX), or 3 (Text)."
