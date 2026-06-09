from datetime import datetime, timezone

from fastapi import HTTPException

from app.data.store import store
from app.models.domain import Booking
from app.schemas import BookingCreate
from app.services.settlement import calculate_payable


def list_bookings() -> list[Booking]:
    return sorted(store.bookings.values(), key=lambda booking: booking.created_at, reverse=True)


def create_booking(payload: BookingCreate) -> Booking:
    slot = store.time_slots.get(payload.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时段不存在")
    if slot.status != "available":
        raise HTTPException(status_code=409, detail="该时段不可预约")

    member = store.members.get(payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="会员不存在")

    original, discount, payable = calculate_payable(slot, member)
    booking_id = store.next_booking_id()
    booking = Booking(
        id=booking_id,
        slot_id=slot.id,
        court_id=slot.court_id,
        member_id=member.id,
        member_name=member.name,
        contact_name=payload.contact_name,
        original_amount=original,
        discount_rate=discount,
        payable_amount=payable,
        status="pending",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    store.bookings[booking_id] = booking
    store.time_slots[slot.id] = slot.model_copy(update={"status": "booked"})
    return booking


def settle_booking(booking_id: int) -> Booking:
    booking = store.bookings.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    if booking.status == "paid":
        return booking
    paid = booking.model_copy(update={"status": "paid"})
    store.bookings[booking_id] = paid
    return paid


def cancel_booking(booking_id: int) -> Booking:
    booking = store.bookings.get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="预约不存在")
    canceled = booking.model_copy(update={"status": "canceled"})
    store.bookings[booking_id] = canceled
    slot = store.time_slots.get(booking.slot_id)
    if slot:
        store.time_slots[slot.id] = slot.model_copy(update={"status": "available"})
    return canceled
