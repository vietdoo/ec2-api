from uuid import UUID

import structlog

from vec2.kit.services import ResourceServiceReader
from vec2.logging import Logger
from vec2.models import OAuthAccount
from vec2.models.user import OAuthPlatform
from vec2.postgres import AsyncSession

log: Logger = structlog.get_logger()


class OAuthAccountService(ResourceServiceReader[OAuthAccount]):
    async def get_by_platform_and_account_id(
        self, session: AsyncSession, platform: OAuthPlatform, account_id: str
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, account_id=account_id)

    async def get_by_platform_and_user_id(
        self, session: AsyncSession, platform: OAuthPlatform, user_id: UUID
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, user_id=user_id)

    async def get_by_platform_and_username(
        self, session: AsyncSession, platform: OAuthPlatform, username: str
    ) -> OAuthAccount | None:
        return await self.get_by(session, platform=platform, account_username=username)


oauth_account_service = OAuthAccountService(OAuthAccount)
