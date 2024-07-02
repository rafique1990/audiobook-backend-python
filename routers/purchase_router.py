from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Purchase, PurchaseCreate, PurchaseRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=PurchaseRead)
def create_purchase(purchase: PurchaseCreate, session: Session = Depends(get_session)):
    db_purchase = Purchase.from_orm(purchase)
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)
    return db_purchase


@router.get("/{purchase_id}", response_model=PurchaseRead)
def read_purchase(purchase_id: int, session: Session = Depends(get_session)):
    purchase = session.get(Purchase, purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.get("/", response_model=List[PurchaseRead])
def list_purchases(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    purchases = session.exec(select(Purchase).offset(skip).limit(limit)).all()
    return purchases


@router.put("/{purchase_id}", response_model=PurchaseRead)
def update_purchase(
    purchase_id: int, purchase: PurchaseCreate, session: Session = Depends(get_session)
):
    db_purchase = session.get(Purchase, purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    purchase_data = purchase.dict(exclude_unset=True)
    for key, value in purchase_data.items():
        setattr(db_purchase, key, value)
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)
    return db_purchase


@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, session: Session = Depends(get_session)):
    purchase = session.get(Purchase, purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    session.delete(purchase)
    session.commit()
    return {"ok": True}
