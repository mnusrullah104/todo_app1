"""
JWT authentication middleware and dependencies.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

ALGORITHM = "HS256"

# Security scheme for Swagger UI
security = HTTPBearer()


class JWTPayload:
    """Decoded JWT token payload"""

    def __init__(self, sub: str, exp: int, iss: str, aud: str):
        self.sub = sub  # User ID
        self.exp = exp  # Expiration timestamp
        self.iss = iss  # Issuer
        self.aud = aud  # Audience

    @property
    def user_id(self) -> UUID:
        """Get user ID as UUID"""
        return UUID(self.sub)

    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.utcnow().timestamp() > self.exp


def decode_jwt(token: str) -> JWTPayload:
    """
    Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        JWTPayload with decoded claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract required claims
        sub = payload.get("sub")
        exp = payload.get("exp")
        iss = payload.get("iss")
        aud = payload.get("aud")

        if not all([sub, exp, iss, aud]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        jwt_payload = JWTPayload(sub=sub, exp=exp, iss=iss, aud=aud)

        # Check expiration
        if jwt_payload.is_expired():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return jwt_payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    """
    FastAPI dependency to extract and validate user ID from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        User ID (UUID)

    Raises:
        HTTPException: If token is missing, invalid, or expired
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_jwt(credentials.credentials)
    return payload.user_id


def verify_user_access(token_user_id: UUID, requested_user_id: UUID) -> None:
    """
    Verify that the authenticated user matches the requested user_id.

    Args:
        token_user_id: User ID from JWT token
        requested_user_id: User ID from request URL/body

    Raises:
        HTTPException: If user IDs don't match (403 Forbidden)
    """
    if token_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match requested user_id",
        )
