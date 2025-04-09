"""add check column to sensorhistory

Revision ID: d1875358a8ff
Revises: c991d80742c7
Create Date: 2025-04-09 17:51:52.108977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Boolean, text


# revision identifiers, used by Alembic.
revision: str = 'd1875358a8ff'
down_revision: Union[str, None] = 'c991d80742c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('sensorhistory', sa.Column('check', Boolean(), nullable=True, server_default=text('false')))



def downgrade():
    op.drop_column('sensorhistory', 'check')
