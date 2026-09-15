"""Mock File Scanner Provider for testing and local dev."""

import time
from datetime import datetime, timezone
from typing import Optional

from integrations.security.file_scanner.base import BaseFileScanner
from integrations.security.file_scanner.models import ScanResult, ScanStatus

# Known EICAR standard anti-virus test signature
EICAR_SIGNATURE = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


class MockFileScanner(BaseFileScanner):
    """Mock file scanner detecting simulated test payloads and suspicious patterns."""

    def __init__(self, force_infected: bool = False, force_suspicious: bool = False) -> None:
        self.force_infected = force_infected
        self.force_suspicious = force_suspicious

    def scan_bytes(self, data: bytes, filename: Optional[str] = None) -> ScanResult:
        start_time = time.time()

        if self.force_infected or EICAR_SIGNATURE in data or b"MALWARE_TEST_STRING" in data:
            duration = int((time.time() - start_time) * 1000)
            return ScanResult(
                status=ScanStatus.INFECTED,
                scanner_name="MockFileScanner",
                threat_name="EICAR_Standard_Test_File",
                threat_category="Virus/TestSignature",
                confidence_score=1.0,
                scan_duration_ms=duration,
                raw_output="FOUND EICAR test signature",
            )

        # Check for suspicious double extensions like invoice.pdf.exe
        if filename:
            lower_name = filename.lower()
            if lower_name.endswith(".exe") or lower_name.endswith(".bat") or lower_name.endswith(".vbs") or ".pdf.exe" in lower_name:
                duration = int((time.time() - start_time) * 1000)
                return ScanResult(
                    status=ScanStatus.INFECTED,
                    scanner_name="MockFileScanner",
                    threat_name="SuspiciousExecutableExtension",
                    threat_category="UnsafeExecutable",
                    confidence_score=0.95,
                    scan_duration_ms=duration,
                    raw_output=f"Blocked dangerous executable extension in filename: {filename}",
                )

        if self.force_suspicious:
            duration = int((time.time() - start_time) * 1000)
            return ScanResult(
                status=ScanStatus.SUSPICIOUS,
                scanner_name="MockFileScanner",
                threat_name="Heuristic.SuspiciousMacro",
                threat_category="SuspiciousHeuristic",
                confidence_score=0.70,
                scan_duration_ms=duration,
                raw_output="Suspicious macro heuristic triggered",
            )

        duration = int((time.time() - start_time) * 1000)
        return ScanResult(
            status=ScanStatus.CLEAN,
            scanner_name="MockFileScanner",
            confidence_score=1.0,
            scan_duration_ms=duration,
            raw_output="No threats detected",
        )

    def scan_file(self, file_path: str) -> ScanResult:
        with open(file_path, "rb") as f:
            data = f.read()
        return self.scan_bytes(data, filename=file_path)
