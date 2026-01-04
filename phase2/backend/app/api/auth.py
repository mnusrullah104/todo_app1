"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    registration: RegisterRequest,
    session: Session = Depends(get_session),
):
    """
    Register a new user account.

    Creates a new user with the provided email and password.
    Returns the user data and a JWT access token.

    - **email**: Valid email address (RFC 5322 format)
    - **password**: Minimum 8 characters
    - **name**: Optional display name
    """
    return await auth_service.register_user(registration, session)


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session),
):
    """
    Authenticate user and return JWT token.

    Validates credentials and returns user data with JWT access token.

    - **email**: Registered email address
    - **password**: User's password
    """
    return await auth_service.login_user(login_data, session)
