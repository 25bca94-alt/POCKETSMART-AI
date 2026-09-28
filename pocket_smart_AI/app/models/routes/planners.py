from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.db_models import History, Planner, User
from app.models.schemas import (
    HistoryResponse,
    PlannerCreate,
    PlannerResponse,
)


router = APIRouter(
    prefix="/api/planners",
    tags=["Planners"],
)


@router.post(
    "",
    response_model=PlannerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_planner(
    planner_data: PlannerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create and save a planner.

    The AI response is initially stored as a placeholder.
    The AI service can be connected here later.
    """

    ai_response = (
        "Your PocketSmartAI plan has been created. "
        "Connect the AI service to generate a personalized plan."
    )

    planner = Planner(
        user_id=current_user.id,
        planner_type=planner_data.planner_type,
        title=planner_data.title,
        input_data=planner_data.input_data,
        ai_response=ai_response,
    )

    db.add(planner)

    history = History(
        user_id=current_user.id,
        planner_type=planner_data.planner_type,
        request_text=planner_data.input_data,
        response_text=ai_response,
    )

    db.add(history)

    db.commit()
    db.refresh(planner)

    return planner


@router.get(
    "",
    response_model=list[PlannerResponse],
)
def get_planners(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all planners belonging to the current user.
    """

    statement = (
        select(Planner)
        .where(Planner.user_id == current_user.id)
        .order_by(Planner.created_at.desc())
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{planner_id}",
    response_model=PlannerResponse,
)
def get_planner(
    planner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return one planner belonging to the current user.
    """

    planner = db.scalar(
        select(Planner).where(
            Planner.id == planner_id,
            Planner.user_id == current_user.id,
        )
    )

    if planner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planner not found.",
        )

    return planner


@router.get(
    "/history/all",
    response_model=list[HistoryResponse],
)
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return planner history for the current user.
    """

    statement = (
        select(History)
        .where(History.user_id == current_user.id)
        .order_by(History.created_at.desc())
    )

    return list(db.scalars(statement).all())