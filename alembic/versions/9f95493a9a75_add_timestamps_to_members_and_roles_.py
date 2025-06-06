"""Add timestamps to members and roles tables

Revision ID: 9f95493a9a75
Revises: 254aaf285d7c
Create Date: 2025-05-27 22:25:31.673904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f95493a9a75'
down_revision: Union[str, None] = '254aaf285d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('games', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('members', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('members', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('roles', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('roles', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'updated_at')
    op.drop_column('roles', 'created_at')
    op.drop_column('members', 'updated_at')
    op.drop_column('members', 'created_at')
    op.drop_column('games', 'updated_at')
    op.drop_column('games', 'created_at')
    # ### end Alembic commands ###
