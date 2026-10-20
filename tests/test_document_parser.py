from io import BytesIO

import pytest
from docx import Document

from app.services.document_parser import (
    DocumentParsingError,
    extract_text,
)


def test_rejects_unsupported_extension():
    with pytest.raises(DocumentParsingError):
        extract_text("resume.txt", b"Some text")


def test_rejects_empty_file():
    with pytest.raises(DocumentParsingError):
        extract_text("resume.pdf", b"")


def test_extracts_docx_text():
    buffer = BytesIO()
    document = Document()
    document.add_paragraph("Python developer")
    document.save(buffer)

    text = extract_text("resume.docx", buffer.getvalue())

    assert "Python developer" in text


def test_rejects_oversized_file():
    with pytest.raises(DocumentParsingError):
        extract_text(
            "resume.pdf",
            b"x" * (5 * 1024 * 1024 + 1),
        )