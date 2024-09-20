import re
from pypdf import PdfReader

class Inputter:
    def __init__(self, filename):
        self.filename = filename

    def clean_text(self, text):
        # Define a pattern to match typical page numbers and footers
        page_number_pattern = re.compile(r"^\s*\d+\s*$|^\s*Page\s+\d+\s*$", re.IGNORECASE)
        footer_pattern = re.compile(r"(footer text|confidential|any pattern you know)", re.IGNORECASE)

        lines = text.splitlines()

        # Filter out lines that match page numbers or footers
        clean_lines = [line for line in lines if not page_number_pattern.match(line.strip()) and not footer_pattern.match(line.strip())]

        # Optional: Remove lines from the start or end if they're too short (common in headers/footers)
        if len(clean_lines) > 2:
            clean_lines = clean_lines[1:-1]  # This removes the first and last line, likely to be headers/footers

        return "\n".join(clean_lines)

    def read(self):
        reader = PdfReader(self.filename)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                clean_text = self.clean_text(text)
                print(clean_text)
                print("-" * 20, "\n")

def main():
    inputter = Inputter("jeff101.pdf")
    inputter.read()

if __name__ == "__main__":
    main()
