"""Contract Repository handling database queries for contracts and commitment baselines."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.contract import (
    Contract,
    ContractApproval,
    ContractBaseline,
    ContractClientAcceptance,
    ContractDiscrepancy,
    ContractSection,
    ContractSignature,
    ContractVersion,
)


class ContractRepository:
    """Repository methods for contracts, versions, approvals, acceptances, signatures, and baselines."""

    @staticmethod
    def get_contract(db: Session, contract_id: uuid.UUID) -> Optional[Contract]:
        return db.query(Contract).filter(Contract.id == contract_id).first()

    @staticmethod
    def list_contracts(
        db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[Contract]:
        query = db.query(Contract)
        if status:
            query = query.filter(Contract.status == status)
        return query.order_by(Contract.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create_contract(db: Session, contract_data: dict) -> Contract:
        contract = Contract(**contract_data)
        db.add(contract)
        db.commit()
        db.refresh(contract)
        return contract

    @staticmethod
    def create_section(db: Session, section_data: dict) -> ContractSection:
        sec = ContractSection(**section_data)
        db.add(sec)
        db.commit()
        db.refresh(sec)
        return sec

    @staticmethod
    def create_approval(db: Session, approval_data: dict) -> ContractApproval:
        appr = ContractApproval(**approval_data)
        db.add(appr)
        db.commit()
        db.refresh(appr)
        return appr

    @staticmethod
    def create_client_acceptance(db: Session, acceptance_data: dict) -> ContractClientAcceptance:
        acc = ContractClientAcceptance(**acceptance_data)
        db.add(acc)
        db.commit()
        db.refresh(acc)
        return acc

    @staticmethod
    def create_signature(db: Session, signature_data: dict) -> ContractSignature:
        sig = ContractSignature(**signature_data)
        db.add(sig)
        db.commit()
        db.refresh(sig)
        return sig

    @staticmethod
    def create_baseline(db: Session, baseline_data: dict) -> ContractBaseline:
        base = ContractBaseline(**baseline_data)
        db.add(base)
        db.commit()
        db.refresh(base)
        return base

    @staticmethod
    def create_discrepancy(db: Session, discrepancy_data: dict) -> ContractDiscrepancy:
        disc = ContractDiscrepancy(**discrepancy_data)
        db.add(disc)
        db.commit()
        db.refresh(disc)
        return disc

    @staticmethod
    def create_version(db: Session, version_data: dict) -> ContractVersion:
        ver = ContractVersion(**version_data)
        db.add(ver)
        db.commit()
        db.refresh(ver)
        return ver
