from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import User
from app.models.schemas import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.routes.session import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new PocketSmartAI user.
    """

    existing_user = db.scalar(
        select(User).where(
            User.email == user_data.email
        )
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address is already registered.",
        )

    user = User(
        name=user_data.name.strip(),
        email=str(user_data.email).lower(),
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT token.
    """

    user = db.scalar(
        select(User).where(
            User.email == str(user_data.email).lower()
        )
    )

    if user is None or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    token = create_access_token(user.id)

    return Token(
        access_token=token,
        token_type="bearer",
    )