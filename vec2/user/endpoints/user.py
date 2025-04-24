from fastapi import Depends

# from vec2.auth.dependencies import Authenticator, WebUser
# from vec2.auth.models import AuthSubject
# from vec2.authz.service import Authz
from vec2.models import User

#Import datetime
from datetime import datetime
# from vec2.postgres import AsyncSession, get_db_session
# from vec2.routing import APIRouter
# from vec2.user.service.user import user as user_service

# from ..schemas.user import UserRead, UserScopes, UserSetAccount
from fastapi import APIRouter
router = APIRouter()

# @router.get("/me", response_model=UserRead)
# async def get_authenticated(auth_subject: WebUser) -> User:
#     return auth_subject.subject


# @router.get("/me/scopes", response_model=UserScopes)
# async def scopes(
#     auth_subject: AuthSubject[User] = Depends(Authenticator(allowed_subjects={User})),
# ) -> UserScopes:
#     return UserScopes(scopes=list(auth_subject.scopes))


# @router.patch("/me/account", response_model=UserRead)
# async def set_account(
#     set_account: UserSetAccount,
#     auth_subject: WebUser,
#     authz: Authz = Depends(Authz.authz),
#     session: AsyncSession = Depends(get_db_session),
# ) -> User:
#     return await user_service.set_account(
#         session,
#         authz=authz,
#         user=auth_subject.subject,
#         account_id=set_account.account_id,
#     )




import random
@router.get("/me")
async def get_user_test():
    return User(
        id = 1,
        email = f"test{random.randint(1, 999)}@example.com",
        hashed_password = "is_active",
        is_active = True,
        created_at = datetime.now(),
    )
    