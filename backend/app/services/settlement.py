from app.models.domain import Member, TimeSlot


def calculate_payable(slot: TimeSlot, member: Member) -> tuple[float, float, float]:
    original = round(slot.price, 2)
    discount = member.discount_rate
    payable = round(original * discount, 2)
    return original, discount, payable
