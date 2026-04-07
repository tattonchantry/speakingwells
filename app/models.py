from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

# Account models
class AccountCreate(BaseModel):
    email: EmailStr
    password: str
    shipping_address: Optional[str] = None

class AccountLogin(BaseModel):
    email: EmailStr
    password: str

class AccountResponse(BaseModel):
    id: UUID
    email: str
    shipping_address: Optional[str]
    created_at: datetime

# Cardholder models
class CardholderCreate(BaseModel):
    name: str
    slug: str
    photo_url: Optional[str] = None
    card_message: Optional[str] = "I want you to know I noticed you and I care about you. Have a great day!"

class CardholderResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    photo_url: Optional[str]
    card_message: str
    created_at: datetime

# Message models
class MessageCreate(BaseModel):
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None
    message_body: str

class MessageResponse(BaseModel):
    id: UUID
    sender_name: Optional[str]
    sender_email: Optional[str]
    message_body: str
    sent_at: datetime

# Card order models
class CardOrderCreate(BaseModel):
    quantity: int

class CardOrderResponse(BaseModel):
    id: UUID
    quantity: int
    status: str
    created_at: datetime
