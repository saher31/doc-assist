from pathlib import Path
import fitz

class PDFTextExtractor:

    def extract_text(self, pdf_path: Path) -> str:
        pages = []

        with fitz.open(pdf_path) as document:
            for page in document:
                pages.append(page.get_text())

        return "\n".join(pages).strip()
        
        
