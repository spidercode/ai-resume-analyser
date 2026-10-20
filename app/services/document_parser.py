from io import BytesIO
from pathlib import Path
import re
import pymupdf
from docx import Document
from sys import exception


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc"}

MAX_FILE_SIZE = 5 * 1024 * 1024 # 50MB

class DocumentParsingError(Exception):
    """Raise when a document cannot be parsed safely"""


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def extract_text(filename: str, file_bytes: bytes) -> str: 
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS: 
        raise DocumentParsingError("Only PDF and DOCX files are supported.")

    if not file_bytes: 
        raise DocumentParsingError("The uploaded file is empty")

    try: 
        if extension == ".pdf":
            with pymupdf.open(stream=file_bytes, filetype="pdf") as document: 
                if document.is_encrypted:
                    raise DocumentParsingError("Cannot open document. Document is encrypted")

                text = "\n\n".join(page.get_text() for page in document)
        else:
            document = Document(BytesIO(file_bytes)) 

            paragraphs = [paragraph.text for paragraph in document.paragraphs]

            for table in document.tables:
                for row in table.rows:
                    paragraphs.append(" | ".join(cell.text for cell in row.cells))
            
            text = "\n".join(paragraphs)
        
    except DocumentParsingError:
        raise
    except Exception as exec:
        raise DocumentParsingError("The document is invalid or could not be parsed.") from exec

    text = clean_text(text)

    if not text: 
        raise DocumentParsingError("No readable text was found. The PDF may be scanned.")

    return text
        
