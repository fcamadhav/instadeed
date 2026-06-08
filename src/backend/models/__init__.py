from pydantic import BaseModel
from typing import Optional

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class SendOTPRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

class GoogleAuthRequest(BaseModel):
    name: str
    email: str
    picture: str = ""

class OrderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str
    service_type: str
    amount: float
    form_data: dict = {}

class VerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

class OfflineOrderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str
    agreement_type: str
    amount: float
    status: str = "COMPLETED"
    form_data: dict = {}

class StatusUpdateRequest(BaseModel):
    status: str

class AdminUpdateUserRequest(BaseModel):
    role: Optional[str] = None
    is_active: Optional[int] = None

class CouponCreateRequest(BaseModel):
    code: str
    type: str = "percentage"
    value: float
    max_uses: int = 0
    min_amount: float = 0
    expires_at: str = ""

class NotificationCreateRequest(BaseModel):
    type: str = "info"
    recipient: str = ""
    title: str = ""
    message: str = ""
    reference_type: str = ""
    reference_id: str = ""

class LeegalitySignRequest(BaseModel):
    order_id: str
    signee_name: str
    signee_email: str
    signee_phone: str
