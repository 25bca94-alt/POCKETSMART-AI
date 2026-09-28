from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =========================================================
# USER SCHEMAS
# =========================================================


class UserBase(BaseModel):
    """
    Common user fields.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr


class UserCreate(UserBase):
    """
    Schema used when registering a new user.
    """

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
    )


class UserLogin(BaseModel):
    """
    Schema used when logging in.
    """

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
    )


class UserResponse(UserBase):
    """
    Public user response.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# AUTHENTICATION SCHEMAS
# =========================================================


class Token(BaseModel):
    """
    JWT authentication response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Data stored inside the JWT token.
    """

    user_id: int


# =========================================================
# PLANNER SCHEMAS
# =========================================================


class PlannerCreate(BaseModel):
    """
    Schema for creating an AI planner request.
    """

    planner_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    input_data: str = Field(
        ...,
        min_length=1,
    )


class PlannerResponse(BaseModel):
    """
    Planner response returned to the frontend.
    """

    id: int
    user_id: int
    planner_type: str
    title: str
    input_data: str
    ai_response: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# HISTORY SCHEMAS
# =========================================================


class HistoryCreate(BaseModel):
    """
    Schema for saving history.
    """

    planner_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    request_text: str = Field(
        ...,
        min_length=1,
    )

    response_text: str = Field(
        ...,
        min_length=1,
    )


class HistoryResponse(BaseModel):
    """
    History response returned to the frontend.
    """

    id: int
    user_id: int
    planner_type: str
    request_text: str
    response_text: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )