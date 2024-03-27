"""create url shortener table

Revision ID: 5f8ae3b396dd
Revises:
Create Date: 2024-03-27 17:11:00.813204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f8ae3b396dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shortened_urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_url', sa.String(length=255), nullable=True),
    sa.Column('short_link', sa.String(length=7), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shortened_urls_short_link'), 'shortened_urls', ['short_link'], unique=True)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shortened_urls_short_link'), table_name='shortened_urls')
    op.drop_table('shortened_urls')
    # ### end Alembic commands ###
