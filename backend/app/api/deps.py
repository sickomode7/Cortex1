from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

def require_admin(x_user_email: str = Header(..., alias="X-User-Email")) -> str:
    """
    Validates that the provided email in the X-User-Email header is an authorized admin.
    """
    if x_user_email not in settings.admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrative privileges."
        )
    return x_user_email


def get_current_user(x_user_id: str = Header(..., alias="X-User-Id"), db: Session = Depends(get_db)) -> User:
    """
    Mock dependency for MVP. 
    In production, this would validate a JWT token and fetch the user.
    """
    try:
        user_uuid = UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid User ID format")
        
    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
