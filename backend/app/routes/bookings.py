from fastapi import APIRouter

from app.models.domain import Booking
from app.schemas import BookingCreate
from app.services import bookings as booking_service

router = APIRouter(tags=["bookings"])


@router.get("/bookings", response_model=list[Booking])
def list_bookings() -> list[Booking]:
    return booking_service.list_bookings()


@router.post("/bookings", response_model=Booking, status_code=201)
def create_booking(payload: BookingCreate) -> Booking:
    return booking_service.create_booking(payload)


@router.post("/bookings/{booking_id}/settle", response_model=Booking)
def settle_booking(booking_id: int) -> Booking:
    return booking_service.settle_booking(booking_id)


@router.post("/bookings/{booking_id}/cancel", response_model=Booking)
def cancel_booking(booking_id: int) -> Booking:
    return booking_service.cancel_booking(booking_id)
