"""Database repository implementations."""

# Future Library
from __future__ import annotations

# Standard Library
import logging

from collections import defaultdict
from contextlib import asynccontextmanager, contextmanager
from enum import StrEnum
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Generator,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    cast,
)

# 3rd Party Library
from sqlalchemy import Insert, Table, select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.postgresql.dml import Insert as PostgresInsert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.sqlite.dml import Insert as SqliteInsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Session

# 1st Party Library
from rwskit.collections_ import is_iterable
from rwskit.sqlalchemy.base import BaseModel, DtoModel
from rwskit.sqlalchemy.engine import (
    AlchemyEngine,
    AsyncAlchemyEngine,
    SyncAlchemyEngine,
)
from rwskit.sqlalchemy.expressions import (
    SqlBinaryExpression,
    SqlOrderCriteria,
    SqlOrderExpression,
    SqlSelectionCriteria,
)

EngineT = TypeVar("EngineT", bound=AlchemyEngine)
"""A generic type for an ``AlchemyEngine``."""


log = logging.getLogger(__name__)

DeclBaseT = TypeVar("DeclBaseT", bound=DeclarativeBase)
"""A type extending :class:`~sqlalchemy.orm.DeclarativeBase`."""

ModelT = TypeVar("ModelT", bound=BaseModel)
"""A generic type for a ``BaseModel``."""


SessionT = TypeVar("SessionT", Session, AsyncSession)
"""A generic type for an sqlalchemy Session."""


class ConflictResolutionStrategy(StrEnum):
    DO_NOTHING = "do_nothing"
    UPDATE = "update"


class IndexElementSet(StrEnum):
    PRIMARY_KEYS = "primary_keys"
    NATURAL_KEYS = "natural_keys"


class Repository(Generic[ModelT, EngineT]):
    """A class implementing the basic find and insert operations for the data access layer."""

    def __init__(self, engine: EngineT, model_class: Type[ModelT]):
        self.engine = engine
        self.model_class = model_class

    def normalize_insert_data(
        self, data: ModelT | Iterable[ModelT]
    ) -> Iterable[ModelT]:
        """Ensure the insert data is always an iterable."""
        if not is_iterable(data):
            data = cast(Iterable[ModelT], [data])

        # The above check ensures that 'data' is iterable, but pylance
        # can't figure that out.
        return cast(Iterable[ModelT], data)

    def _make_upsert_statements(
        self,
        data: ModelT | Iterable[ModelT],
        on_conflict: ConflictResolutionStrategy,
        index_element_set: Iterable[str] | IndexElementSet,
    ) -> list[Insert]:
        """
        Create upsert statements for each type of ``BaseModel`` found when
        walking the data.
        """
        instances: Iterable[ModelT] = self.normalize_insert_data(data)

        # Recursively traverse each instance and any children, i.e.,
        # relationships, to dictionaries and group the converted instances
        # by their type. We do the conversion and grouping in one method
        # because it is easier to implement this way using
        # 'BaseModel.walk_children'. Although the input items should all be
        # of 'ModelT', the resulting items could be of any type derived from
        # 'BaseModel'.
        grouped_values = self._convert_to_dict_and_group_by_type(instances)

        # Sort the groups by their insertion order so that we will insert
        # items with no dependencies before items with dependencies.
        grouped_values = self._sort_instances_by_insertion_order(grouped_values)

        # Create an alias to make the list comprehension more readable.
        make_stmt = self._make_upsert_statement

        return [
            make_stmt(m, v, on_conflict, index_element_set)
            for m, v in grouped_values.items()
        ]

    def _make_upsert_statement(
        self,
        model_class: Type[BaseModel],
        model_values: list[dict[str, Any]],
        on_conflict: Optional[ConflictResolutionStrategy],
        index_element_set: Iterable[str] | IndexElementSet,
    ) -> Insert:
        def _get_insert_function() -> Callable[..., PostgresInsert | SqliteInsert]:
            if self.engine.dialect == "postgresql":
                return postgres_insert
            elif self.engine.dialect == "sqlite":
                return sqlite_insert
            else:
                raise ValueError(
                    f"The dialect '{self.engine.dialect}' does not support 'upserts'"
                )

        insert = _get_insert_function()

        if index_element_set == IndexElementSet.PRIMARY_KEYS:
            index_elements = model_class.primary_key_column_names()
        elif index_element_set == IndexElementSet.NATURAL_KEYS:
            index_elements = model_class.natural_key_column_names()
        else:
            index_elements: set[str] = set(index_element_set)

        # The base insert
        stmt = insert(model_class).values(model_values)

        if on_conflict == ConflictResolutionStrategy.DO_NOTHING:
            stmt = stmt.on_conflict_do_nothing(index_elements=index_elements)
        elif on_conflict == ConflictResolutionStrategy.UPDATE:
            stmt = stmt.on_conflict_do_update(
                index_elements=index_elements,
                set_={c.name: c for c in stmt.excluded if c.name not in index_elements},
            )
        else:
            raise ValueError(f"Invalid 'on_conflict' value: {on_conflict}")

        return stmt

    @classmethod
    def _convert_to_dict_and_group_by_type(
        cls, data: Iterable[BaseModel]
    ) -> dict[Type[BaseModel], list[dict[str, Any]]]:
        result: dict[Type[BaseModel], list[dict[str, Any]]] = defaultdict(list)

        def add_to_result(node: BaseModel):
            """Convert the node to a dictionary and add it to the result."""
            column_names = [str(c.key) for c in node.table_columns()]
            lookup_attr_name = node.get_attribute_name_from_column_name
            attr_names = [lookup_attr_name(c) for c in column_names]
            value: dict[str, Any] = {a: getattr(node, a, None) for a in attr_names}
            result[node.__class__].append(value)

        for item in data:
            item.walk_children(add_to_result, traverse_viewonly=False)

        return result

    @classmethod
    def _sort_instances_by_insertion_order(
        cls, data: dict[Type[BaseModel], list[dict[str, Any]]]
    ) -> dict[Type[BaseModel], list[dict[str, Any]]]:
        order_lookup = BaseModel.table_insertion_order()

        def _get_table_order(entry: tuple[Type[BaseModel], Any]) -> int:
            return order_lookup[cast(Table, entry[0].__table__)]

        return {k: v for k, v in sorted(data.items(), key=_get_table_order)}

    def _make_select_statement(
        self,
        filter_by: Iterable[SqlBinaryExpression],
        order_by: Iterable[SqlOrderExpression],
        limit: Optional[int] = None,
    ):
        filter_criteria = SqlSelectionCriteria(list(filter_by))
        order_criteria = SqlOrderCriteria(list(order_by))

        return (
            select(self.model_class)
            .where(filter_criteria.to_conjunction(self.model_class))
            .order_by(*order_criteria.to_criteria(self.model_class))
            .limit(limit)
        )


class SyncRepository(Repository[ModelT, SyncAlchemyEngine]):
    # region API
    def merge(
        self, instances: ModelT | Iterable[ModelT], session: Optional[Session] = None
    ):
        """
        Insert one or more model instances into the database.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The data to insert.
        session : Session, optional
            A session to use.

        Raises
        ------
        Exception
            If there is a problem adding the data to the database.
        """
        instances = self.normalize_insert_data(instances)

        with self.get_or_create_session(session) as local_session:
            for instance in instances:
                local_session.merge(instance)

    def insert(
        self, instances: ModelT | Iterable[ModelT], session: Optional[Session] = None
    ):
        """
        Insert one or more model instances into the database.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The data to insert.
        session : Session, optional
            A session to use.

        Raises
        ------
        Exception
            If there is a problem adding the data to the database.
        """
        instances = self.normalize_insert_data(instances)

        with self.get_or_create_session(session) as local_session:
            local_session.add_all(instances)

    def upsert(
        self,
        instances: ModelT | Iterable[ModelT],
        on_conflict: ConflictResolutionStrategy = ConflictResolutionStrategy.DO_NOTHING,
        index_set: Iterable[str] | IndexElementSet = IndexElementSet.PRIMARY_KEYS,
        session: Optional[Session] = None,
    ):
        """
        Upsert one or more model instances into the database.

        ..note::
            This only works with dialects that support INSERT ... ON CONFLICT.
            This should include ``postgresql``, ``mysql/mariadb``, and
            ``sqlite``. However, currently only ``postgresql`` is supported.

        ..note::
            This method creates several copies of the data, so you should be
            careful about memory management if you are inserting a large number
            of objects.

        ..warning::
            This only works if all non-null fields are provided **including
            primary and foreign keys.**

        ..warning::
            This is not well tested with complex model configurations such as
            hybrid properties and column properties.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The instances to upsert.
        on_conflict : ConflictResolutionStrategy
            The conflict resolution strategy (e.g., 'do nothing' or 'update')
        index_set : Iterable[str] | IndexElementSet
            The set of columns to use for the ``index_elements``.
        session : Session, optional
            An optional session to use instead of creating a new one.

        Raises
        ------
        OperationalError
            If the ``index_set`` does not correspond to a collection of columns
            that have a unique index defined on them.
        """
        upsert_statements = self._make_upsert_statements(
            instances, on_conflict, index_set
        )

        # The for loop could be around or inside the 'get_or_create_session'
        # method. It would be more efficient to have it inside, but for large
        # collections it might cause problems.
        for stmt in upsert_statements:
            with self.get_or_create_session(session) as local_session:
                local_session.execute(stmt)

    def find_all_models(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        order_by: Iterable[SqlOrderExpression] = (),
        limit: Optional[int] = None,
        session: Optional[Session] = None,
    ) -> list[ModelT]:
        """
        Finds and retrieves multiple models from the database based on specified
        filters, ordering, and a limit. Converts the retrieved models to their
        corresponding DTO (Data Transfer Object) representation.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Collection of SQL binary expressions defining the conditions for
            filtering the query. Default is an empty iterable.
        order_by : Iterable[SqlOrderExpression], optional
            Collection of SQL order expressions defining the sorting order for the
            query. Default is an empty iterable.
        limit : int, optional
            Maximum number of records to retrieve. If None, no limit is applied.
            Default is None.
        session : Session, optional
            An optional database session instance. If not provided, a new session
            will be created internally for executing the query.

        Returns
        -------
        list[DtoModel]
            A list of DTO instances that correspond to the retrieved database models.
        """
        stmt = self._make_select_statement(filter_by, order_by, limit)

        with self.get_or_create_session(session) as local_session:
            result = local_session.scalars(stmt)
            models = list(result.all())

        return models

    def find_all_dtos(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        order_by: Iterable[SqlOrderExpression] = (),
        limit: Optional[int] = None,
        session: Optional[Session] = None,
    ) -> list[DtoModel]:
        """
        Finds and retrieves multiple models from the database based on specified
        filters, ordering, and a limit. Converts the retrieved models to their
        corresponding DTO (Data Transfer Object) representation.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Collection of SQL binary expressions defining the conditions for
            filtering the query. Default is an empty iterable.
        order_by : Iterable[SqlOrderExpression], optional
            Collection of SQL order expressions defining the sorting order for the
            query. Default is an empty iterable.
        limit : int, optional
            Maximum number of records to retrieve. If None, no limit is applied.
            Default is None.
        session : Session, optional
            An optional database session instance. If not provided, a new session
            will be created internally for executing the query.

        Returns
        -------
        list[DtoModel]
            A list of DTO instances that correspond to the retrieved database models.
        """
        stmt = self._make_select_statement(filter_by, order_by, limit)

        with self.get_or_create_session(session) as local_session:
            result = local_session.scalars(stmt)
            models = result.all()
            dtos = [m.to_dto() for m in models]

        return dtos

    def find_one_model(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        session: Optional[Session] = None,
        raise_on_none: bool = True,
    ) -> Optional[ModelT]:
        """
        Retrieve a single record from the database that matches the provided filter
        criteria. An exception is raised when more than one result is returned or no
        results are found when `raise_on_none` is True.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Filter conditions to apply when querying the database. Defaults to an
            empty tuple.

        session : Optional[Session], optional
            SQLAlchemy session to use for querying. If not provided, a new session
            will be created and used for the operation.

        raise_on_none : bool, optional
            Specifies whether to raise an exception if no records match the specified
            filter criteria. Defaults to True.

        Returns
        -------
        ModelT
            The retrieved data model if a record is found; otherwise, ``None``
            when ``raise_on_none`` is set to False.

        """
        # 'find_one' doesn't need an 'order_by', because it will be an exception
        # if more than one result is found by the query.
        stmt = self._make_select_statement(filter_by, ())
        with self.get_or_create_session(session) as local_session:
            result = local_session.scalars(stmt)
            model = result.one() if raise_on_none else result.one_or_none()

        return model

    def find_one_dto(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        session: Optional[Session] = None,
        raise_on_none: bool = True,
    ) -> Optional[DtoModel]:
        """
        Retrieve a single record from the database that matches the provided filter
        criteria. Converts the obtained database model into a data transfer object
        (DTO). An exception is raised when more than one result is returned or no
        results are found when `raise_on_none` is True.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Filter conditions to apply when querying the database. Defaults to an
            empty tuple.

        session : Optional[Session], optional
            SQLAlchemy session to use for querying. If not provided, a new session
            will be created and used for the operation.

        raise_on_none : bool, optional
            Specifies whether to raise an exception if no records match the specified
            filter criteria. Defaults to True.

        Returns
        -------
        DtoModel
            The retrieved data model in DTO form if a record is found; otherwise, ``None``
            when ``raise_on_none`` is set to False.

        """
        # 'find_one' doesn't need an 'order_by', because it will be an exception
        # if more than one result is found by the query.
        stmt = self._make_select_statement(filter_by, ())
        with self.get_or_create_session(session) as local_session:
            result = local_session.scalars(stmt)
            model = result.one() if raise_on_none else result.one_or_none()
            dto = model.to_dto() if model is not None else None

        return dto

    # endregion API

    # region Helpers
    @contextmanager
    def get_or_create_session(self, session: Optional[Session]) -> Generator[Session]:
        """
        Use the existing session if it is not ``None``, otherwise create and
        return a new one.

        Parameters
        ----------
        session : Optional[Session], default=``None``
            An existing session to use.

        Yields
        ------
        Generator[Session]
            The existing or new session as a context manager.
        """
        if session is None:
            with self.engine.session_scope() as engine_session:
                yield engine_session
        else:
            yield session

    # endregion Helpers


class AsyncRepository(Repository[ModelT, AsyncAlchemyEngine]):
    # region API
    async def merge(
        self,
        instances: ModelT | Iterable[ModelT],
        session: Optional[AsyncSession] = None,
    ):
        """
        Insert one or more model instances into the database.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The data to insert.
        session : AsyncSession, optional
            A session to use.

        Raises
        ------
        Exception
            If there is a problem adding the data to the database.
        """
        instances = self.normalize_insert_data(instances)

        async with self.get_or_create_session(session) as local_session:
            for instance in instances:
                await local_session.merge(instance)

    async def insert(
        self,
        instances: ModelT | Iterable[ModelT],
        session: Optional[AsyncSession] = None,
    ):
        """
        Insert one or more model instances into the database.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The data to insert.
        session : AsyncSession, optional
            A session to use.

        Raises
        ------
        Exception
            If there is a problem adding the data to the database.
        """
        instances = self.normalize_insert_data(instances)

        async with self.get_or_create_session(session) as local_session:
            local_session.add_all(instances)

    async def upsert(
        self,
        instances: ModelT | Iterable[ModelT],
        on_conflict: ConflictResolutionStrategy = ConflictResolutionStrategy.DO_NOTHING,
        index_set: Iterable[str] | IndexElementSet = IndexElementSet.PRIMARY_KEYS,
        session: Optional[AsyncSession] = None,
    ):
        """
        Upsert one or more model instances into the database.

        ..note::
            This only works with dialects that support INSERT ... ON CONFLICT.
            This should include ``postgresql``, ``mysql/mariadb``, and
            ``sqlite``. However, currently only ``postgresql`` is supported.

        ..note::
            This method creates several copies of the data, so you should be
            careful about memory management if you are inserting a large number
            of objects.

        ..warning::
            This only works if all non-null fields are provided **including
            primary and foreign keys.**

        ..warning::
            This is not well tested with complex model configurations such as
            hybrid properties and column properties.

        Parameters
        ----------
        instances : ModelT | Iterable[ModelT]
            The instances to upsert.
        on_conflict : ConflictResolutionStrategy
            The conflict resolution strategy (e.g., 'do nothing' or 'update')
        index_set : Iterable[str] | IndexElementSet
            The set of columns to use for the ``index_elements``.
        session : AsyncSession, optional
            An optional session to use instead of creating a new one.

        Raises
        ------
        OperationalError
            If the ``index_set`` does not correspond to a collection of columns
            that have a unique index defined on them.
        """
        upsert_statements = self._make_upsert_statements(
            instances, on_conflict, index_set
        )

        # The for loop could be around or inside the 'get_or_create_session'
        # method. It would be more efficient to have it inside, but for large
        # collections it might cause problems.
        for stmt in upsert_statements:
            async with self.get_or_create_session(session) as local_session:
                await local_session.execute(stmt)

    async def find_all_models(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        order_by: Iterable[SqlOrderExpression] = (),
        limit: Optional[int] = None,
        session: Optional[AsyncSession] = None,
    ) -> list[ModelT]:
        """
        Finds and retrieves multiple models from the database based on specified
        filters, ordering, and a limit. Converts the retrieved models to their
        corresponding DTO (Data Transfer Object) representation.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Collection of SQL binary expressions defining the conditions for
            filtering the query. Default is an empty iterable.
        order_by : Iterable[SqlOrderExpression], optional
            Collection of SQL order expressions defining the sorting order for the
            query. Default is an empty iterable.
        limit : int, optional
            Maximum number of records to retrieve. If None, no limit is applied.
            Default is None.
        session : AsyncSession, optional
            An optional database session instance. If not provided, a new session
            will be created internally for executing the query.

        Returns
        -------
        list[DtoModel]
            A list of DTO instances that correspond to the retrieved database models.
        """
        stmt = self._make_select_statement(filter_by, order_by, limit)

        async with self.get_or_create_session(session) as local_session:
            result = await local_session.scalars(stmt)
            models = list(result.all())

        return models

    async def find_all_dtos(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        order_by: Iterable[SqlOrderExpression] = (),
        limit: Optional[int] = None,
        session: Optional[AsyncSession] = None,
    ) -> list[DtoModel]:
        """
        Finds and retrieves multiple models from the database based on specified
        filters, ordering, and a limit. Converts the retrieved models to their
        corresponding DTO (Data Transfer Object) representation.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Collection of SQL binary expressions defining the conditions for
            filtering the query. Default is an empty iterable.
        order_by : Iterable[SqlOrderExpression], optional
            Collection of SQL order expressions defining the sorting order for the
            query. Default is an empty iterable.
        limit : int, optional
            Maximum number of records to retrieve. If None, no limit is applied.
            Default is None.
        session : AsyncSession, optional
            An optional database session instance. If not provided, a new session
            will be created internally for executing the query.

        Returns
        -------
        list[DtoModel]
            A list of DTO instances that correspond to the retrieved database models.
        """
        stmt = self._make_select_statement(filter_by, order_by, limit)

        async with self.get_or_create_session(session) as local_session:
            result = await local_session.scalars(stmt)
            models = result.all()
            dtos = [m.to_dto() for m in models]

        return dtos

    async def find_one_model(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        session: Optional[AsyncSession] = None,
        raise_on_none: bool = True,
    ) -> Optional[ModelT]:
        """
        Retrieve a single record from the database that matches the provided filter
        criteria. An exception is raised when more than one result is returned or no
        results are found when `raise_on_none` is True.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Filter conditions to apply when querying the database. Defaults to an
            empty tuple.

        session : Optional[Session], optional
            SQLAlchemy session to use for querying. If not provided, a new session
            will be created and used for the operation.

        raise_on_none : bool, optional
            Specifies whether to raise an exception if no records match the specified
            filter criteria. Defaults to True.

        Returns
        -------
        ModelT
            The retrieved data model if a record is found; otherwise, ``None``
            when ``raise_on_none`` is set to False.

        """
        # 'find_one' doesn't need an 'order_by', because it will be an exception
        # if more than one result is found by the query.
        stmt = self._make_select_statement(filter_by, ())
        async with self.get_or_create_session(session) as local_session:
            result = await local_session.scalars(stmt)
            model = result.one() if raise_on_none else result.one_or_none()

        return model

    async def find_one_dto(
        self,
        filter_by: Iterable[SqlBinaryExpression] = (),
        session: Optional[AsyncSession] = None,
        raise_on_none: bool = True,
    ) -> Optional[DtoModel]:
        """
        Retrieve a single record from the database that matches the provided filter
        criteria. Converts the obtained database model into a data transfer object
        (DTO). An exception is raised when more than one result is returned or no
        results are found when `raise_on_none` is True.

        Parameters
        ----------
        filter_by : Iterable[SqlBinaryExpression], optional
            Filter conditions to apply when querying the database. Defaults to an
            empty tuple.

        session : Optional[Session], optional
            SQLAlchemy session to use for querying. If not provided, a new session
            will be created and used for the operation.

        raise_on_none : bool, optional
            Specifies whether to raise an exception if no records match the specified
            filter criteria. Defaults to True.

        Returns
        -------
        DtoModel
            The retrieved data model in DTO form if a record is found; otherwise, ``None``
            when ``raise_on_none`` is set to False.

        """
        # 'find_one' doesn't need an 'order_by', because it will be an exception
        # if more than one result is found by the query.
        stmt = self._make_select_statement(filter_by, ())
        async with self.get_or_create_session(session) as local_session:
            result = await local_session.scalars(stmt)
            model = result.one() if raise_on_none else result.one_or_none()
            dto = model.to_dto() if model is not None else None

        return dto

    # endregion API

    # region Helpers
    @asynccontextmanager
    async def get_or_create_session(
        self, session: Optional[AsyncSession]
    ) -> AsyncGenerator[AsyncSession]:
        """
        Use the existing session if it is not ``None``, otherwise create and
        return a new one.

        Parameters
        ----------
        session : AsyncSession], optional
            An existing session to use.

        Yields
        ------
        AsyncGenerator[AsyncSession]
            The existing or new session as a context manager.
        """
        if session is None:
            async with self.engine.session_scope() as engine_session:
                yield engine_session
        else:
            yield session

    # endregion Helpers
