from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class PaymentType(str, Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    KES = "KES"
    UGX = "UGX"
    TZS = "TZS"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Customer(BaseModel):
    email: str
    name: str
    phone: Optional[str] = None

class Transaction(BaseModel):
    id: str
    amount: float
    currency: Currency
    status: TransactionStatus
    payment_type: PaymentType
    customer: Customer
    created_at: str
    updated_at: str
    metadata: Optional[dict] = Field(default_factory=dict)

class CheckoutSession(BaseModel):
    id: str
    amount: float
    currency: Currency
    payment_type: PaymentType
    customer: Customer
    status: TransactionStatus
    checkout_url: str
    created_at: str
    expires_at: str
    metadata: Optional[dict] = Field(default_factory=dict) 