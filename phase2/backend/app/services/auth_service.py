"""
Authentication service for user registration and login.
"""
from sqlmodel import Session, select
from fastapi import HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from uuid import UUID
import os

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse, AuthResponse
from app.utils.security import hash_password, verify_password

# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7  # 7 days as specified


# Simulated password storage (in production, Better Auth handles this)
# For Phase II, we'll store hashed passwords in a separate table or use Better Auth
# This is a simplified implementation for demonstration
_password_store: dict[str, str] = {}


def create_access_token(user_id: UUID, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User's UUID
        expires_delta: Optional expiration time delta (default: 7 days)

    Returns:
        Encoded JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    expire = datetime.utcnow() + expires_delta
    base_url = os.getenv("NEXT_PUBLIC_BASE_URL", "http://localhost:3000")

    to_encode = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()),
        "iss": base_url,
        "aud": base_url,
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(
    registration: RegisterRequest, session: Session
) -> AuthResponse:
    """
    Register a new user.

    Args:
        registration: User registration data
        session: Database session

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException: If email already exists (400)
    """
    # Check if user already exists
    statement = select(User).where(User.email == registration.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    new_user = User(
        email=registration.email,
        name=registration.name,
        email_verified=False,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Store hashed password (simplified for Phase II)
    _password_store[str(new_user.id)] = hash_password(registration.password)

    # Generate JWT token
    token = create_access_token(new_user.id)

    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        token=token,
    )


async def login_user(login: LoginRequest, session: Session) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    Args:
        login: Login credentials
        session: Database session

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException: If credentials are invalid (401)
    """
    # Find user by email
    statement = select(User).where(User.email == login.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password (simplified for Phase II)
    stored_password = _password_store.get(str(user.id))
    if not stored_password or not verify_password(login.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate JWT token
    token = create_access_token(user.id)

    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=token,
    )
