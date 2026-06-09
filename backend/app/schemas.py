from pydantic import BaseModel, Field


class CourtCreate(BaseModel):
    name: str = Field(min_length=1)
    surface: str = Field(min_length=1)
    indoor: bool = True


class TimeSlotCreate(BaseModel):
    court_id: int
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    label: str = Field(min_length=3)
    price: float = Field(gt=0)


class TimeSlotUpdate(BaseModel):
    price: float | None = Field(default=None, gt=0)
    status: str | None = Field(default=None, pattern="^(available|blocked|booked)$")


class BookingCreate(BaseModel):
    slot_id: int
    member_id: int = 1
    contact_name: str = Field(min_length=1)
