"""change id

Revision ID: b69acf25ffba
Revises: 4a03e406957f
Create Date: 2024-07-17 19:21:37.237729

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b69acf25ffba"
down_revision: Union[str, None] = "4a03e406957f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Add a temporary UUID column
    op.add_column("file_upload", sa.Column("temp_id", sa.UUID(), nullable=False))

    # Populate the temporary column with new UUIDs
    op.execute("UPDATE file_upload SET temp_id = gen_random_uuid()")

    # Drop the old id column
    op.drop_column("file_upload", "id")

    # Rename temp_id to id
    op.alter_column(
        "file_upload",
        "temp_id",
        new_column_name="id",
        existing_type=sa.UUID(),
        existing_nullable=False,
    )

    # Set id as primary key
    op.create_primary_key("pk_file_upload", "file_upload", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("file_upload", sa.Column("temp_id", sa.Integer(), nullable=False))

    op.execute("UPDATE file_upload SET temp_id = id")

    op.drop_column("file_upload", "id")

    op.alter_column(
        "file_upload",
        "temp_id",
        new_column_name="id",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )

    op.create_primary_key("pk_file_upload", "file_upload", ["id"])
    # ### end Alembic commands ###
