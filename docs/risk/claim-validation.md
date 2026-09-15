# Claim Validation Subsystem

## Overview
Personalized AI communication often generates claims regarding a target business's performance, digital presence, or competitive standing. The Claim Validation Subsystem evaluates claims against strict truthfulness and evidence rules.

## Evaluated Categories

1. **Guarantees**: Absolute outcome promises ("100% success", "double your revenue") are prohibited and flagged with `CRITICAL` severity (`BLOCK`).
2. **Fabricated Social Proof**: Unverified claims regarding client numbers ("hundreds of clients") trigger `CRITICAL` severity (`BLOCK`).
3. **False Urgency**: Artificial expiration deadlines or artificial slot limits trigger `HIGH` severity (`REVIEW`).
4. **Deceptive Identity**: Misleading subject lines ("Re: your order") trigger `CRITICAL` severity (`BLOCK`).
5. **Invented Facts**: Unverified statistics regarding revenue losses or competitor superiority require supporting evidence.
