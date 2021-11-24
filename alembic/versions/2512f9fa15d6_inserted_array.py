"""Inserted array

Revision ID: 2512f9fa15d6
Revises: e20b89a5efcd
Create Date: 2021-11-24 21:20:12.470830

"""
from alembic import op
import sqlalchemy as sa

import sys
sys.path = ['', '..'] + sys.path[1:]

from application.database import db_session
from application.models import Feature

# revision identifiers, used by Alembic.
revision = '2512f9fa15d6'
down_revision = 'e20b89a5efcd'
branch_labels = None
depends_on = None


def upgrade():
    feature = Feature(
        values=[1.2, 1.5, 1.1],
        value_name="x",
        index=0
    )

    db_session.add(feature)
    db_session.commit()
    


def downgrade():
    pass
