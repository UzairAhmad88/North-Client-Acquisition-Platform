"""File validation and security verification engine."""

import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.documents.base import FileValidationResult

# Magic bytes signature map
MAGIC_SIGNATURES: Dict[str, bytes] = {
    "pdf": b"%PDF-",
    "png": b"\x89PNG\r\n\x1a\n",
    "jpeg": b"\xff\xd8\xff",
    "gif": b"GIF8",
    "zip": b"PK\x03\x04",
    "tar": b"ustar",
}

BLOCKED_EXTENSIONS = {
    ".exe", ".bat", ".cmd", ".vbs", ".ps1", ".sh", ".dll", ".so",
    ".dylib", ".msi", ".com", ".scr", ".pif", ".application", ".gadget"
}

MAX_FILE_SIZE_DEFAULT = 100 * 1024 * 1024  # 100 MB


class FileValidator:
    """Validates binary integrity, MIME types, signatures, and blocks dangerous payloads."""

    def __init__(self, max_size_bytes: int = MAX_FILE_SIZE_DEFAULT) -> None:
        self.max_size_bytes = max_size_bytes

    def validate_file_content(
        self,
        filename: str,
        data: bytes,
        declared_mime_type: Optional[str] = None,
    ) -> FileValidationResult:
        errors: List[str] = []
        lower_name = filename.lower()
        size_bytes = len(data)

        # 1. Size check
        if size_bytes == 0:
            errors.append("File is empty (0 bytes).")
        elif size_bytes > self.max_size_bytes:
            errors.append(f"File size {size_bytes} exceeds limit of {self.max_size_bytes} bytes.")

        # 2. Check for double extension or dangerous executables (e.g. invoice.pdf.exe)
        is_executable = False
        for blocked_ext in BLOCKED_EXTENSIONS:
            if lower_name.endswith(blocked_ext):
                is_executable = True
                errors.append(f"Executable file extension '{blocked_ext}' is strictly prohibited.")
                break

        if ".pdf.exe" in lower_name or ".docx.exe" in lower_name or ".xlsx.exe" in lower_name:
            is_executable = True
            errors.append("Dangerous obfuscated executable filename detected.")

        # 3. Path & extension analysis
        path_obj = Path(filename)
        ext = path_obj.suffix.lower()

        # 4. MIME sniffing and signature validation
        guessed_mime, _ = mimetypes.guess_type(filename)
        effective_mime = declared_mime_type or guessed_mime or "application/octet-stream"

        if ext == ".pdf":
            if not data.startswith(MAGIC_SIGNATURES["pdf"]):
                errors.append("File declared as PDF does not have valid '%PDF-' header signature.")
        elif ext in [".png"]:
            if not data.startswith(MAGIC_SIGNATURES["png"]):
                errors.append("File declared as PNG does not have valid PNG header signature.")
        elif ext in [".jpg", ".jpeg"]:
            if not data.startswith(MAGIC_SIGNATURES["jpeg"]):
                errors.append("File declared as JPEG does not have valid JPEG header signature.")

        checksum = hashlib.sha256(data).hexdigest()

        return FileValidationResult(
            is_valid=len(errors) == 0,
            mime_type=effective_mime,
            detected_extension=ext,
            size_bytes=size_bytes,
            checksum_sha256=checksum,
            is_executable=is_executable,
            validation_errors=errors,
        )
