from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.base import ExecutableOption

from vec2.kit.utils import utc_now

from .db.models import RecordModel
from .db.postgres import AsyncSession, sql
from .schemas import Schema

ModelType = TypeVar("ModelType", bound=RecordModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)
SchemaType = TypeVar("SchemaType", bound=Schema)


class ResourceServiceReader(
    Generic[ModelType],
):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(
        self,
        session: AsyncSession,
        id: UUID,
        allow_deleted: bool = False,
        *,
        options: Sequence[ExecutableOption] | None = None,
    ) -> ModelType | None:
        query = sql.select(self.model).where(self.model.id == id)
        if not allow_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        if options is not None:
            query = query.options(*options)
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()

    async def get_by(self, session: AsyncSession, **clauses: Any) -> ModelType | None:
        query = sql.select(self.model).filter_by(**clauses)
        res = await session.execute(query)
        return res.scalars().unique().one_or_none()

    async def soft_delete(self, session: AsyncSession, id: UUID) -> None:
        stmt = (
            sql.update(self.model)
            .where(self.model.id == id, self.model.deleted_at.is_(None))
            .values(
                deleted_at=utc_now(),
            )
        )
        await session.execute(stmt)
        await session.flush()


class ResourceService(
    ResourceServiceReader[ModelType],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
):
    # Ideally, actions would only contain class methods since there is
    # no state to retain. Unable to achieve this with mapping the model
    # and schema as class attributes though without breaking typing.

    # TODO: Investigate new bulk methods in SQLALchemy 2.0 for upsert_many
    async def upsert_many(
        self,
        session: AsyncSession,
        create_schemas: list[CreateSchemaType],
        constraints: list[InstrumentedAttribute[Any]],
        mutable_keys: set[str],
        autocommit: bool = True,
    ) -> Sequence[ModelType]:
        return await self._db_upsert_many(
            session,
            create_schemas,
            constraints=constraints,
            mutable_keys=mutable_keys,
            autocommit=autocommit,
        )

    async def _db_upsert_many(
        self,
        session: AsyncSession,
        objects: list[CreateSchemaType],
        constraints: list[InstrumentedAttribute[Any]],
        mutable_keys: set[str],
        autocommit: bool = True,
    ) -> Sequence[ModelType]:
        values = [obj.model_dump(by_alias=True) for obj in objects]
        if not values:
            raise ValueError("Zero values provided")

        insert_stmt = sql.insert(self.model).values(values)

        # Update the insert statement with what to update on conflict, i.e mutable keys.
        upsert_stmt = (
            insert_stmt.on_conflict_do_update(
                index_elements=constraints,
                set_={k: getattr(insert_stmt.excluded, k) for k in mutable_keys},
            )
            .returning(self.model)
            .execution_options(populate_existing=True)
        )

        res = await session.execute(upsert_stmt)
        instances = res.scalars().all()
        if autocommit:
            await session.commit()
        return instances
