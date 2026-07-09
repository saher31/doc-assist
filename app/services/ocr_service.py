import fitz
import easyocr
import numpy as np
import torch
import logging

logger = logging.getLogger("uvicorn.error")


class OCRService:
    OCR_DPI = 300

    def __init__(self):
        self.reader = easyocr.Reader(
            ["en", "ar"],
            gpu=self._should_use_gpu(),
        )

    def _should_use_gpu(self) -> bool:
        if torch.backends.mps.is_available():
            logger.info("EasyOCR is running on Apple Silicon GPU (MPS)")
            return True

        if torch.cuda.is_available():
            logger.info("EasyOCR is running on NVIDIA GPU (CUDA)")
            return True

        logger.info("EasyOCR is running on CPU")
        return False

    def extract_page(self, page: fitz.Page) -> str:
        image = self._page_to_image(page)
        return self._extract_text(image)

    def _page_to_image(self, page: fitz.Page) -> np.ndarray:
        pixmap = page.get_pixmap(dpi=self.OCR_DPI)

        image = np.frombuffer(
            pixmap.samples,
            dtype=np.uint8,
        ).reshape(
            pixmap.height,
            pixmap.width,
            pixmap.n,
        )


        if pixmap.n == 4:
            image = image[:, :, :3]

        return image

    def _extract_text(self, image: np.ndarray) -> str:
        results = self.reader.readtext(
            image,
            detail=0,
            paragraph=True,
        )

        return "\n".join(results).strip()