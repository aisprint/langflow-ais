"""Add error and edit flags to message

Revision ID: eb5e72293a8e
Revises: 5ace73a7f223
Create Date: 2024-09-19 16:18:50.828648

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "eb5e72293a8e"
down_revision: Union[str, None] = "5ace73a7f223"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("message")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("message", schema=None) as batch_op:
        if "error" not in column_names:
            batch_op.add_column(sa.Column("error", sa.Boolean(), nullable=False, server_default=sa.false()))
        if "edit" not in column_names:
            batch_op.add_column(sa.Column("edit", sa.Boolean(), nullable=False, server_default=sa.false()))

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("message")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("message", schema=None) as batch_op:
        if "edit" in column_names:
            batch_op.drop_column("edit")
        if "error" in column_names:
            batch_op.drop_column("error")

    # ### end Alembic commands ###
