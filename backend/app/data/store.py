from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from app.models.domain import Booking, Court, Member, TimeSlot
from app.services.settlement import calculate_payable


class InMemoryStore:
    def __init__(self) -> None:
        self.courts: dict[int, Court] = {}
        self.members: dict[int, Member] = {}
        self.time_slots: dict[int, TimeSlot] = {}
        self.bookings: dict[int, Booking] = {}
        self._next_slot_id = 1
        self._next_booking_id = 1
        self._seed()

    def next_booking_id(self) -> int:
        booking_id = self._next_booking_id
        self._next_booking_id += 1
        return booking_id

    def next_slot_id(self) -> int:
        slot_id = self._next_slot_id
        self._next_slot_id += 1
        return slot_id

    def _create_booking(
        self,
        slot: TimeSlot,
        member: Member,
        contact_name: str,
        status: str,
        created_at: str,
    ) -> Booking:
        original, discount, payable = calculate_payable(slot, member)
        booking_id = self.next_booking_id()
        booking = Booking(
            id=booking_id,
            slot_id=slot.id,
            court_id=slot.court_id,
            member_id=member.id,
            member_name=member.name,
            contact_name=contact_name,
            original_amount=original,
            discount_rate=discount,
            payable_amount=payable,
            status=status,
            created_at=created_at,
        )
        self.bookings[booking_id] = booking
        if status in ("pending", "paid"):
            self.time_slots[slot.id] = slot.model_copy(update={"status": "booked"})
        return booking

    def _seed(self) -> None:
        self.courts = {
            1: Court(id=1, name="A1 标准场", surface="木地板", indoor=True),
            2: Court(id=2, name="A2 标准场", surface="木地板", indoor=True),
            3: Court(id=3, name="B1 训练场", surface="PVC", indoor=True),
            4: Court(id=4, name="C1 竞赛场", surface="专业地胶", indoor=True),
        }
        self.members = {
            1: Member(id=1, name="散客", level="普通", discount_rate=1.0, phone=""),
            2: Member(id=2, name="李明", level="银卡", discount_rate=0.9, phone="13800000001"),
            3: Member(id=3, name="王悦", level="金卡", discount_rate=0.8, phone="13800000002"),
            4: Member(id=4, name="陈教练", level="教练", discount_rate=0.7, phone="13800000003"),
        }

        hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "19:00-21:00"]
        today = date.today()
        for day_offset in range(7):
            current_day = today + timedelta(days=day_offset)
            for court in self.courts.values():
                for index, label in enumerate(hours):
                    price = 60.0 if index < 2 else 80.0
                    if label == "19:00-21:00":
                        price = 120.0
                    slot_id = self.next_slot_id()
                    self.time_slots[slot_id] = TimeSlot(
                        id=slot_id,
                        court_id=court.id,
                        date=current_day.isoformat(),
                        label=label,
                        price=price,
                        status="available",
                    )

        today_iso = today.isoformat()
        slots_by_key = {
            (slot.court_id, slot.date, slot.label): slot
            for slot in self.time_slots.values()
        }

        blocked_slots = [
            (1, today_iso, "08:00-10:00"),
            (2, today_iso, "14:00-16:00"),
            (3, today_iso, "19:00-21:00"),
        ]
        for court_id, date_str, label in blocked_slots:
            slot = slots_by_key.get((court_id, date_str, label))
            if slot:
                self.time_slots[slot.id] = slot.model_copy(update={"status": "blocked"})

        now = datetime.now(timezone.utc)

        pending_bookings = [
            ((1, today_iso, "10:00-12:00"), 2, "李明"),
            ((4, today_iso, "16:00-18:00"), 1, "张先生"),
        ]
        for (court_id, date_str, label), member_id, contact_name in pending_bookings:
            slot = slots_by_key.get((court_id, date_str, label))
            member = self.members.get(member_id)
            if slot and member:
                created_at = (now - timedelta(minutes=30)).isoformat()
                self._create_booking(slot, member, contact_name, "pending", created_at)

        paid_bookings = [
            ((2, today_iso, "10:00-12:00"), 3, "王悦"),
            ((1, today_iso, "16:00-18:00"), 4, "陈教练"),
            ((4, today_iso, "19:00-21:00"), 2, "李明"),
        ]
        for (court_id, date_str, label), member_id, contact_name in paid_bookings:
            slot = slots_by_key.get((court_id, date_str, label))
            member = self.members.get(member_id)
            if slot and member:
                created_at = (now - timedelta(hours=2)).isoformat()
                self._create_booking(slot, member, contact_name, "paid", created_at)

        canceled_bookings = [
            ((3, today_iso, "10:00-12:00"), 1, "刘女士"),
            ((2, today_iso, "16:00-18:00"), 3, "王悦"),
        ]
        for (court_id, date_str, label), member_id, contact_name in canceled_bookings:
            slot = slots_by_key.get((court_id, date_str, label))
            member = self.members.get(member_id)
            if slot and member:
                created_at = (now - timedelta(hours=5)).isoformat()
                self._create_booking(slot, member, contact_name, "canceled", created_at)


store = InMemoryStore()
