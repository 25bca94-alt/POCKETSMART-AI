from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import HTTPException


router = APIRouter(
    tags=["Pages"],
)


# Project root:
# PocketSmartAI/
#     app/
#     frontend/
#
# parents[0] = app/
# parents[1] = PocketSmartAI/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def get_frontend_file(filename: str) -> FileResponse:
    """
    Return a frontend HTML file safely.
    """

    file_path = FRONTEND_DIR / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Frontend file '{filename}' was not found.",
        )

    return FileResponse(
        path=str(file_path),
        media_type="text/html",
    )


@router.get("/")
def home():
    return get_frontend_file("index.html")


@router.get("/login")
def login_page():
    return get_frontend_file("login.html")


@router.get("/register")
def register_page():
    return get_frontend_file("register.html")


@router.get("/home-planner")
def home_planner_page():
    return get_frontend_file("home_planner.html")


@router.get("/jewelry-planner")
def jewelry_planner_page():
    return get_frontend_file("jewelry_planner.html")


@router.get("/party-planner")
def party_planner_page():
    return get_frontend_file("party_planner.html")


@router.get("/history")
def history_page():
    return get_frontend_file("history.html")