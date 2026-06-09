from fastapi import APIRouter

from app.models.domain import Member
from app.services import members as member_service

router = APIRouter(tags=["members"])


@router.get("/members", response_model=list[Member])
def list_members() -> list[Member]:
    return member_service.list_members()
