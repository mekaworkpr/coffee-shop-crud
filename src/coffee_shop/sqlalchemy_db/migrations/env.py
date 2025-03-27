import asyncio
from logging import getLogger
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, MetaData
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from coffee_shop.settings import settings
from coffee_shop.sqlalchemy_db.base import Base
from coffee_shop.sqlalchemy_db.init_models import init_models

logger = getLogger(__name__)

init_models()

config = context.config

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def do_run_migrations(connection: Connection) -> None:
    metadata: MetaData = Base.metadata
    context.configure(
        connection=connection, target_metadata=metadata, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

    logger.info(f"[Alembic] Tables: {", ".join(metadata.tables.keys())}")


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


asyncio.run(run_migrations_online())
