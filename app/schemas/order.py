from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.order import OrderStatus

class OrderBase(BaseModel):
    user_id: int
    document_id: Optional[int] = None
    amount: float = Field(..., ge=0.0)
    status: OrderStatus = OrderStatus.PENDING
    payment_id: Optional[str] = None
    form_data: Optional[Dict[str, Any]] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_id: Optional[str] = None

class OrderInDBBase(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderResponse(OrderInDBBase):
    pass
