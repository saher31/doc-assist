# DocAssist 

This is a minimal implementation of a RAG (Retrieval-Augmented Generation) application for question answering from PDF documents using semantic search and Google Gemini.

## Requirements
- python 3.10 or later

#### Install python using conda
1) Install miniconda or anaconda from [here](https://docs.conda.io/en/latest/miniconda.html)
2) Create a new environment
```bash
conda create -n doc-assist python=3.11
```
3) Activate the environment
```bash
conda activate doc-assist
```

## Installation

### Install the required packages
```bash
pip install -r requirements.txt
```

### Setup the environment variables
```bash
cp .env.example .env
```
Set your environment variables in the `.env` file. Like `GEMINI_API_KEY` value.

## RUN docker compose Services

```bash
docker compose up -d
```

## Run the FastAPI server
```bash
cd app
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## OCR Support

DocAssist automatically falls back to OCR when PyMuPDF cannot extract readable text from a PDF page. This is handled by the `TextExtractionService` which detects pages that need OCR based on:

- **No text extracted** — the page is likely a scanned image.
- **Garbled text** — the extracted text has a low ratio of meaningful characters.
- **Full-page image with few words** — the page is mostly an image with minimal embedded text.

### How it works

1. Each page is first processed with **PyMuPDF** for fast, native text extraction.
2. If the result is empty, garbled, or the page is image-heavy, the page is rendered as a **300 DPI image** and passed to **EasyOCR**.
3. EasyOCR extracts text with support for **Arabic** and **English**.


## API Reference

You can explore and test the API directly via the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
