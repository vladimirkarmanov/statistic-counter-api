from core.migrations import apply_alembic_migrations
from core.settings import Settings

settings = Settings()

apply_alembic_migrations(verbose=settings.DEBUG)
