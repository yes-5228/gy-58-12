from app.data.store import store
from app.models.domain import Member


def list_members() -> list[Member]:
    return list(store.members.values())
