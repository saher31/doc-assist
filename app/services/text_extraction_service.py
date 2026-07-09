import logging
from pathlib import Path

import fitz

from services.ocr_service import OCRService

logger = logging.getLogger("uvicorn.error")


class TextExtractionService:
    IMAGE_COVERAGE_THRESHOLD = 0.85

    def __init__(self):
        self.ocr_service = OCRService()

    def extract_text(self, pdf_path: Path) -> str:
        pages = []

        with fitz.open(pdf_path) as document:
            for page in document:
                text = self._extract_with_pymupdf(page)

                if self._should_use_ocr(page, text):
                    logger.info("Using OCR for page %s", page.number + 1)
                    text = self._extract_with_ocr(page)
                else:
                    logger.info("Using PyMuPDF for page %s", page.number + 1)

                pages.append(text)

        return "\n".join(pages).strip()

    def _extract_with_pymupdf(self, page: fitz.Page) -> str:
        return page.get_text().strip()

    def _should_use_ocr(self, page: fitz.Page, text: str) -> bool:
        text = text.strip()

        if not text:
            logger.debug("OCR reason: no text extracted")
            return True

        if self._is_garbled(text):
            logger.debug("OCR reason: garbled text")
            return True

        if self._has_full_page_image(page) and len(text.split()) < 20:
            logger.debug("OCR reason: page is mostly an image with few words")
            return True

        return False

    def _is_garbled(self, text: str) -> bool:
        if not text:
            return True

        meaningful = sum(char.isalnum() for char in text)
        ratio = meaningful / len(text)

        return ratio < 0.4

    def _has_full_page_image(self, page: fitz.Page) -> bool:
        page_area = page.rect.width * page.rect.height
        if page_area == 0:
            return False

        for image in page.get_images(full=True):
            try:
                bbox = page.get_image_bbox(image)
            except ValueError:
                continue

            image_area = bbox.width * bbox.height

            if image_area / page_area >= self.IMAGE_COVERAGE_THRESHOLD:
                return True

        return False

    def _extract_with_ocr(self, page: fitz.Page) -> str:
        return self.ocr_service.extract_page(page)