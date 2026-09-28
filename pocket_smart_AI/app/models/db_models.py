from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """
    User database model.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    planners: Mapped[list["Planner"]] = relationship(
        "Planner",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    history: Mapped[list["History"]] = relationship(
        "History",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Planner(Base):
    """
    Planner database model.

    Stores AI-generated planning information such as
    home, jewelry, and party plans.
    """

    __tablename__ = "planners"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    planner_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    ai_response: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="planners",
    )


class History(Base):
    """
    Stores a record of previous AI planner requests.
    """

    __tablename__ = "history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    planner_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    request_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="history",
    )