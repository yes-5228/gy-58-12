from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import bookings, courts, members

app = FastAPI(title="Badminton Booking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courts.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
