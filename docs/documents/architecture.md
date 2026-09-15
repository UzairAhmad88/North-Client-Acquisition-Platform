# Architecture — Unified Document, File & Digital Asset Management

## 1. Architectural Philosophy

Phase 39 enforces the architectural boundary:

```text
┌──────────────────────────────────────────────────────────────┐
│ FILE                                                         │
│ Raw binary asset + storage key + mime + checksum (SHA-256)    │
└──────────────────────────────┬───────────────────────────────┘
                               │ Promoted with meaning & metadata
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ MANAGED DOCUMENT                                             │
│ Identity + Classification + Permissions + Versions + Reviews  │
└──────────────────────────────┬───────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            ▼                  ▼                  ▼
     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
     │  EVIDENCE   │    │ DELIVERABLE │    │  KNOWLEDGE  │
     │ QA/UAT/Sign │    │  Handover   │    │  Canonical  │
     └─────────────┘    └─────────────┘    └─────────────┘
```

A file uploaded to a project workspace is merely an asset until it is explicitly classified, authorized, reviewed, and promoted to an authoritative state.

---

## 2. End-to-End Processing Pipeline

```text
Upload Request (multipart/form-data)
       │
       ▼
[Authentication & Tenant Isolation]
       │
       ▼
[File Validator] ──► MIME check, magic bytes verification, extension block (.exe, .pdf.exe)
       │
       ▼
[Malware & Security Scanner] ──► Mock / ClamAV Scanner (Detects EICAR & heuristics)
       │   └── If infected ──► Status: QUARANTINED (Blocked from availability)
       ▼
[SHA-256 Checksum Calculation]
       │
       ▼
[Storage Provider Layer] ──► Partitioned tenant object storage (Local / S3)
       │
       ▼
[Text Extraction Engine] ──► Native parser / OCR abstraction (Outputs structured chunks)
       │
       ▼
[Preview Generator] ──► Generates sanitized preview derivatives
       │
       ▼
[Global Search & AI Retrieval] ──► Indexing into Phase 38 Discovery Layer
```

---

## 3. Storage Provider Abstraction

All file storage interactions pass through `BaseStorageProvider`:

```python
class BaseStorageProvider(ABC):
    def upload(storage_key: str, data: bytes, content_type: str) -> StorageObjectMetadata
    def download(storage_key: str) -> bytes
    def delete(storage_key: str) -> bool
    def exists(storage_key: str) -> bool
    def generate_private_url(storage_key: str, expires_in_seconds: int) -> str
    def copy(source_key: str, destination_key: str) -> StorageObjectMetadata
    def move(source_key: str, destination_key: str) -> StorageObjectMetadata
```

No raw disk filepaths or provider credentials are ever leaked to frontend clients or external APIs.
