from fastapi import APIRouter

from app.models.domain import Court, TimeSlot
from app.schemas import CourtCreate, TimeSlotCreate, TimeSlotUpdate
from app.services import courts as court_service

router = APIRouter(tags=["courts"])


@router.get("/courts", response_model=list[Court])
def list_courts() -> list[Court]:
    return court_service.list_courts()


@router.post("/courts", response_model=Court, status_code=201)
def create_court(payload: CourtCreate) -> Court:
    return court_service.create_court(payload)


@router.get("/time-slots", response_model=list[TimeSlot])
def list_time_slots(date: str | None = None, court_id: int | None = None) -> list[TimeSlot]:
    return court_service.list_time_slots(date=date, court_id=court_id)


@router.post("/time-slots", response_model=TimeSlot, status_code=201)
def create_time_slot(payload: TimeSlotCreate) -> TimeSlot:
    return court_service.create_time_slot(payload)


@router.patch("/time-slots/{slot_id}", response_model=TimeSlot)
def update_time_slot(slot_id: int, payload: TimeSlotUpdate) -> TimeSlot:
    return court_service.update_time_slot(slot_id, payload)
