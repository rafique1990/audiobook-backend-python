from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Subscription, SubscriptionCreate, SubscriptionRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=SubscriptionRead)
def create_subscription(
    subscription: SubscriptionCreate, session: Session = Depends(get_session)
):
    db_subscription = Subscription.from_orm(subscription)
    session.add(db_subscription)
    session.commit()
    session.refresh(db_subscription)
    return db_subscription


@router.get("/{subscription_id}", response_model=SubscriptionRead)
def read_subscription(subscription_id: int, session: Session = Depends(get_session)):
    subscription = session.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.get("/", response_model=List[SubscriptionRead])
def list_subscriptions(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    subscriptions = session.exec(select(Subscription).offset(skip).limit(limit)).all()
    return subscriptions


@router.put("/{subscription_id}", response_model=SubscriptionRead)
def update_subscription(
    subscription_id: int,
    subscription: SubscriptionCreate,
    session: Session = Depends(get_session),
):
    db_subscription = session.get(Subscription, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription_data = subscription.dict(exclude_unset=True)
    for key, value in subscription_data.items():
        setattr(db_subscription, key, value)
    session.add(db_subscription)
    session.commit()
    session.refresh(db_subscription)
    return db_subscription


@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: int, session: Session = Depends(get_session)):
    subscription = session.get(Subscription, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    session.delete(subscription)
    session.commit()
    return {"ok": True}
