# Signature Integration Architecture

## Overview
The Signature Integration Subsystem provides an abstract signature provider framework supporting both local mock electronic signatures (`REAL_SIGNATURE=false`) and future enterprise digital signature providers (DocuSign, HelloSign/Dropbox Sign, Adobe Sign).

---

## Provider Abstraction (`BaseSignatureProvider`)

```python
class BaseSignatureProvider(ABC):
    @abstractmethod
    async def create_signature_request(
        self, contract: Contract, version: ContractVersion, signers: List[Dict[str, Any]]
    ) -> SignatureRequestResult:
        pass

    @abstractmethod
    async def verify_signature_status(self, provider_reference: str) -> SignatureStatusResult:
        pass
```

---

## Mock Provider vs Real Signature Configuration

### Mock Signature Provider (`MockSignatureProvider`)
Used during development, staging, testing, and non-enterprise environments:
* Set `SIGNATURE_PROVIDER=mock` and `REAL_SIGNATURE=false`.
* Instantly generates mock signature tokens, verification hashes, and audit events.
* Allows complete contract execution flow testing without third-party API dependencies.

### Production Enterprise Providers
When integrating external signature services:
* Set `SIGNATURE_PROVIDER=docusign` (or `hellosign`).
* `REAL_SIGNATURE=true`.
* Provides webhook event callbacks for `envelope.sent`, `envelope.viewed`, `envelope.completed`, and `envelope.declined`.

---

## Signature Entity (`ContractSignature`)

| Attribute | Type | Purpose |
|---|---|---|
| `signature_id` | UUID | Primary key |
| `contract_id` | UUID | Contract reference |
| `version_id` | UUID | Specific version signed |
| `signer_role` | Enum | `OPERATOR_SIGNER` or `CLIENT_SIGNER` |
| `signer_name` | String | Legal name |
| `signer_email` | String | Verified email |
| `provider` | String | `MOCK` or `DOCUSIGN` |
| `provider_reference` | String | External envelope/request ID |
| `status` | Enum | `PENDING`, `SIGNED`, `DECLINED`, `EXPIRED` |
| `signature_hash` | String | Cryptographic verification hash |
| `signed_at` | DateTime | Signature completion timestamp |
