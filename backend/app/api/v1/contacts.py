import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import AppError
from app.models.user import User
from app.repositories.contact import ContactRepository
from app.schemas.common import DataResponse
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["Contacts CRM"])


@router.post("", response_model=DataResponse[ContactResponse], status_code=201)
def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = ContactRepository.create(db, data.model_dump())
    return {"data": ContactResponse.model_validate(contact)}


@router.get("", response_model=DataResponse[List[ContactResponse]])
def list_contacts(
    business_id: Optional[uuid.UUID] = Query(default=None),
    lead_id: Optional[uuid.UUID] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if lead_id:
        contacts = ContactRepository.list_by_lead(db, lead_id)
    elif business_id:
        contacts = ContactRepository.list_by_business(db, business_id)
    else:
        contacts = []

    return {"data": [ContactResponse.model_validate(c) for c in contacts]}


@router.get("/{contact_id}", response_model=DataResponse[ContactResponse])
def get_contact(
    contact_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = ContactRepository.get_by_id(db, contact_id)
    if not contact:
        raise AppError(
            code="CONTACT_NOT_FOUND", message="Contact record not found.", status_code=404
        )
    return {"data": ContactResponse.model_validate(contact)}


@router.patch("/{contact_id}", response_model=DataResponse[ContactResponse])
def update_contact(
    contact_id: uuid.UUID,
    data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = ContactRepository.get_by_id(db, contact_id)
    if not contact:
        raise AppError(
            code="CONTACT_NOT_FOUND", message="Contact record not found.", status_code=404
        )

    updated = ContactRepository.update(db, contact, data.model_dump(exclude_unset=True))
    return {"data": ContactResponse.model_validate(updated)}


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = ContactRepository.get_by_id(db, contact_id)
    if not contact:
        raise AppError(
            code="CONTACT_NOT_FOUND", message="Contact record not found.", status_code=404
        )

    ContactRepository.delete(db, contact)
    return {"data": {"message": "Contact deleted successfully."}}
