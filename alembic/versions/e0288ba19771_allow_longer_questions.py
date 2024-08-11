"""Allow longer questions

Revision ID: e0288ba19771
Revises: b40dcb1c92cd
Create Date: 2024-08-11 19:45:46.760767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0288ba19771'
down_revision: Union[str, None] = 'b40dcb1c92cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'text',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=300),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'text',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
