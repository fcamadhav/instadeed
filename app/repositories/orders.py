from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        result = await self.db.execute(select(Order).filter(Order.id == order_id))
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        result = await self.db.execute(
            select(Order).filter(Order.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, order_in: OrderCreate) -> Order:
        db_order = Order(
            user_id=order_in.user_id,
            document_id=order_in.document_id,
            amount=order_in.amount,
            status=order_in.status,
            payment_id=order_in.payment_id,
            form_data=order_in.form_data
        )
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def update(self, order_id: int, order_in: OrderUpdate) -> Optional[Order]:
        db_order = await self.get_by_id(order_id)
        if not db_order:
            return None
            
        update_data = order_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
            
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order
