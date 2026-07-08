# Material Take-Off (MTO) Generator

## Overview

The Material Take-Off (MTO) Generator is a web application that automatically extracts piping information from isometric drawings and generates a Material Take-Off (MTO) sheet in Excel format.

Instead of manually reading engineering drawings, this application uses OCR and AI to identify important details such as pipe size, material, valves, elbows, tees, reducers, flanges, and other piping components.

The generated information is then organized into a structured MTO table that can be downloaded as an Excel file.

---

## Features

- Upload PDF or image drawings
- Automatic OCR text extraction using EasyOCR
- AI-based component extraction using Ollama (LLaVA)
- Automatic Material Take-Off generation
- Excel report generation
- Simple and responsive user interface
- FastAPI backend with Next.js frontend

---

## Tech Stack

### Frontend

- Next.js
- TypeScript
- CSS

### Backend

- FastAPI
- Python

### AI & OCR

- EasyOCR
- Ollama
- LLaVA

### Other Libraries

- OpenCV
- pdf2image
- OpenPyXL
- Requests

---

## Project Structure

```
MTO-generation/

│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   └── styles/
│
├── backend/
│   ├── app.py
│   ├── ai.py
│   ├── ocr.py
│   ├── mto.py
│   ├── excel.py
│   ├── uploads/
│   └── outputs/
│
└── README.md
```

## Supported File Formats

- PDF
- PNG
- JPG
- JPEG

---

## Output

The application provides:

- OCR Extracted Text
- AI Extracted Data
- Material Take-Off Table
- Excel Report

---
## Learning Outcomes

This project helped in understanding:

- OCR using EasyOCR
- AI model integration with Ollama
- FastAPI backend development
- Next.js frontend development
- REST API communication
- Excel report generation
- File upload handling
- Image preprocessing with OpenCV

---

## Author

**Gauri**

AI & Machine Learning Enthusiast

---

## License

This project is created for educational and learning purposes.