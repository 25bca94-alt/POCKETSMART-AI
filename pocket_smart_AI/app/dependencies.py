from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


def get_database() -> Generator[Session, None, None]:
    """
    Provide a database session to FastAPI routes.
    """
    yield from get_db()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_database),
) -> User:
    """
    Get the currently authenticated user from a JWT token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        try:
            user_id_int = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.get(User, user_id_int)

    if user is None:
        raise credentials_exception

    return user