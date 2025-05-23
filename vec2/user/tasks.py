import uuid

from vec2.exceptions import vec2TaskError
from vec2.worker import AsyncSessionMaker, JobContext, task

from .service.user import user as user_service


class UserTaskError(vec2TaskError): ...


class UserDoesNotExist(UserTaskError):
    def __init__(self, user_id: uuid.UUID) -> None:
        self.user_id = user_id
        message = f"The user with id {user_id} does not exist."
        super().__init__(message)


@task("user.on_after_signup")
async def user_on_after_signup(ctx: JobContext, user_id: uuid.UUID) -> None:
    async with AsyncSessionMaker(ctx) as session:
        user = await user_service.get(session, user_id)

        if user is None:
            raise UserDoesNotExist(user_id)
