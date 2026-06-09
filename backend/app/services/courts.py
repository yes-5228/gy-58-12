from fastapi import HTTPException

from app.data.store import store
from app.models.domain import Court, TimeSlot
from app.schemas import CourtCreate, TimeSlotCreate, TimeSlotUpdate


def list_courts() -> list[Court]:
    return list(store.courts.values())


def create_court(payload: CourtCreate) -> Court:
    court_id = max(store.courts.keys(), default=0) + 1
    court = Court(id=court_id, **payload.model_dump())
    store.courts[court_id] = court
    return court


def list_time_slots(date: str | None = None, court_id: int | None = None) -> list[TimeSlot]:
    slots = list(store.time_slots.values())
    if date:
        slots = [slot for slot in slots if slot.date == date]
    if court_id:
        slots = [slot for slot in slots if slot.court_id == court_id]
    return sorted(slots, key=lambda slot: (slot.date, slot.court_id, slot.label))


def create_time_slot(payload: TimeSlotCreate) -> TimeSlot:
    if payload.court_id not in store.courts:
        raise HTTPException(status_code=404, detail="场地不存在")
    slot_id = store.next_slot_id()
    slot = TimeSlot(id=slot_id, status="available", **payload.model_dump())
    store.time_slots[slot_id] = slot
    return slot


def update_time_slot(slot_id: int, payload: TimeSlotUpdate) -> TimeSlot:
    slot = store.time_slots.get(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="时段不存在")
    update_data = payload.model_dump(exclude_unset=True)
    next_status = update_data.get("status")
    if slot.status == "booked" and next_status and next_status != "booked":
        raise HTTPException(status_code=409, detail="已预约时段不可直接变更状态")
    updated = slot.model_copy(update=update_data)
    store.time_slots[slot_id] = updated
    return updated
