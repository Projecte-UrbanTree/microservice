import pytest
import os
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
