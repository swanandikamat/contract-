import io
from pathlib import Path
from typing import Union, List, Dict, Any
import docx
from backend.app.utils.text_cleaner import clean_text

class DocumentParser:
    """
    Handles text and metadata extraction from DOCX, PDF, and TXT files,
    preserving structural location (page numbers, section headers) for evidence grounding.
    """
    
    @staticmethod
    def parse_file(file_path_or_bytes: Union[str, Path, bytes], filename: str) -> Dict[str, Any]:
        """
        Parses document source and returns raw text along with structured location-aware pages/sections.
        Returns:
            {
                "filename": str,
                "raw_text": str,
                "pages": List[Dict[str, Any]]  # [{ "page_num": int, "text": str }]
            }
        """
        ext = filename.lower().split('.')[-1]
        
        if ext == 'docx':
            return DocumentParser._parse_docx(file_path_or_bytes, filename)
        elif ext == 'pdf':
            return DocumentParser._parse_pdf(file_path_or_bytes, filename)
        elif ext in ['txt', 'md']:
            return DocumentParser._parse_txt(file_path_or_bytes, filename)
        else:
            raise ValueError(f"Unsupported file format '.{ext}'. Supported formats: .docx, .pdf, .txt")

    @staticmethod
    def _parse_docx(file_source: Union[str, Path, bytes], filename: str) -> Dict[str, Any]:
        if isinstance(file_source, bytes):
            doc = docx.Document(io.BytesIO(file_source))
        else:
            doc = docx.Document(str(file_source))
            
        paragraphs = []
        for p in doc.paragraphs:
            txt = p.text.strip()
            if txt:
                paragraphs.append(txt)
                
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
                    
        full_text = clean_text("\n\n".join(paragraphs))
        
        return {
            "filename": filename,
            "raw_text": full_text,
            "pages": [{"page_num": 1, "text": full_text}]
        }

    @staticmethod
    def _parse_pdf(file_source: Union[str, Path, bytes], filename: str) -> Dict[str, Any]:
        pages_content = []
        
        try:
            import pdfplumber
            if isinstance(file_source, bytes):
                with pdfplumber.open(io.BytesIO(file_source)) as pdf:
                    for i, page in enumerate(pdf.pages, start=1):
                        t = page.extract_text()
                        if t:
                            pages_content.append({"page_num": i, "text": clean_text(t)})
            else:
                with pdfplumber.open(str(file_source)) as pdf:
                    for i, page in enumerate(pdf.pages, start=1):
                        t = page.extract_text()
                        if t:
                            pages_content.append({"page_num": i, "text": clean_text(t)})
        except Exception:
            import fitz
            if isinstance(file_source, bytes):
                doc = fitz.open(stream=file_source, filetype="pdf")
            else:
                doc = fitz.open(str(file_source))
            for i, page in enumerate(doc, start=1):
                t = page.get_text()
                if t:
                    pages_content.append({"page_num": i, "text": clean_text(t)})
                
        full_text = "\n\n".join([p["text"] for p in pages_content])
        if not pages_content:
            pages_content = [{"page_num": 1, "text": full_text}]
            
        return {
            "filename": filename,
            "raw_text": full_text,
            "pages": pages_content
        }

    @staticmethod
    def _parse_txt(file_source: Union[str, Path, bytes], filename: str) -> Dict[str, Any]:
        if isinstance(file_source, bytes):
            text = file_source.decode('utf-8', errors='ignore')
        else:
            with open(file_source, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        cleaned = clean_text(text)
        return {
            "filename": filename,
            "raw_text": cleaned,
            "pages": [{"page_num": 1, "text": cleaned}]
        }
