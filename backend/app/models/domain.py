from pydantic import BaseModel, Field


class Court(BaseModel):
    id: int
    name: str
    surface: str
    indoor: bool = True


class Member(BaseModel):
    id: int
    name: str
    level: str
    discount_rate: float = Field(ge=0.0, le=1.0)
    phone: str = ""


class TimeSlot(BaseModel):
    id: int
    court_id: int
    date: str
    label: str
    price: float
    status: str = "available"


class Booking(BaseModel):
    id: int
    slot_id: int
    court_id: int
    member_id: int
    member_name: str
    contact_name: str
    original_amount: float
    discount_rate: float
    payable_amount: float
    status: str = "pending"
    created_at: str
