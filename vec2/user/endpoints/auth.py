from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from vec2.models.user import User as UserModel
from vec2.user.schemas.user import UserRead, UserCreate
from vec2.auth.utils import hash_password, verify_password, create_access_token, decode_access_token
from vec2.postgres import get_db_session
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

router = APIRouter()

# OAuth2 scheme for JWT via Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    user_id = payload["sub"]
    user = await db.execute(
        UserModel.__table__.select().where(UserModel.id == user_id)
    )
    user = user.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    existing = await db.execute(
        UserModel.__table__.select().where(UserModel.email == user.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    new_user = UserModel(email=user.email, hashed_password=hashed, is_active=True)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserRead(
        id=new_user.id,
        email=new_user.email,
        is_active=new_user.is_active,
        accepted_terms_of_service=False,
        oauth_accounts=[],
        avatar_url=None,
        account_id=None,
        created_at=new_user.created_at,
        updated_at=new_user.created_at
    )

@router.post("/login")
async def login(email: EmailStr, password: str, db: AsyncSession = Depends(get_db_session)):
    user = await db.execute(
        UserModel.__table__.select().where(UserModel.email == email)
    )
    user = user.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        accepted_terms_of_service=False,
        oauth_accounts=[],
        avatar_url=None,
        account_id=None,
        created_at=current_user.created_at,
        updated_at=current_user.created_at
    )
