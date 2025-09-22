"""
Database configuration and session management.
Handles SQLAlchemy engine, session creation, and database utilities.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create the SQLAlchemy declarative base
Base = declarative_base()

# Naming convention for constraints (helpful for Alembic migrations)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s", 
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

# Async engine for FastAPI endpoints
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=20,
    max_overflow=30,
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)

# Synchronous engine for migrations and background tasks
sync_engine = create_engine(
    settings.database_url_sync,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
)

# Synchronous session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


async def get_db() -> AsyncSession:
    """
    Dependency function to get async database session.

    Yields:
        AsyncSession: Database session for async operations
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """
    Get synchronous database session.
    Used for migrations and background tasks.

    Yields:
        Session: Database session for sync operations
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Sync database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def create_tables():
    """Create database tables using async engine."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_tables():
    """Drop all database tables using async engine."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped successfully")


async def check_db_connection():
    """
    Check database connection health.

    Returns:
        bool: True if connection is healthy, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


class DatabaseManager:
    """Database manager for handling connections and health checks."""

    def __init__(self):
        self.async_engine = async_engine
        self.sync_engine = sync_engine

    async def startup(self):
        """Initialize database connections on startup."""
        try:
            # Test async connection
            is_healthy = await check_db_connection()
            if is_healthy:
                logger.info("Database connection established successfully")
            else:
                logger.error("Failed to establish database connection")
                raise ConnectionError("Cannot connect to database")

        except Exception as e:
            logger.error(f"Database startup failed: {e}")
            raise

    async def shutdown(self):
        """Clean up database connections on shutdown."""
        try:
            await self.async_engine.dispose()
            self.sync_engine.dispose()
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Database shutdown error: {e}")


# Global database manager instance
db_manager = DatabaseManager()
