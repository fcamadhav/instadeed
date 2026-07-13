from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.repositories.orders import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
# Note: Ideally you'd have a get_current_user dependency here for authorization

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    repo = OrderRepository(db)
    order = await repo.create(order_in)
    return order

@router.get("/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(user_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    repo = OrderRepository(db)
    orders = await repo.get_by_user_id(user_id, skip=skip, limit=limit)
    return orders

@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order_in: OrderUpdate, db: AsyncSession = Depends(get_db)):
    repo = OrderRepository(db)
    updated_order = await repo.update(order_id, order_in)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
