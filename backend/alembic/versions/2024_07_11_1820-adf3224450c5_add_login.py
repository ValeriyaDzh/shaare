"""add login

Revision ID: adf3224450c5
Revises: ef88072acdd3
Create Date: 2024-07-11 18:20:05.733925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adf3224450c5'
down_revision: Union[str, None] = 'ef88072acdd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'login')
    # ### end Alembic commands ###