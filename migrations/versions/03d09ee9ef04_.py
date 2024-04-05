"""empty message

Revision ID: 03d09ee9ef04
Revises: 2afd7d992644
Create Date: 2024-04-05 20:09:35.322946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03d09ee9ef04'
down_revision = '2afd7d992644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('movie_title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_favorite_movie_id'), ['movie_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_favorite_movie_title'), ['movie_title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_favorite_movie_title'))
        batch_op.drop_index(batch_op.f('ix_favorite_movie_id'))

    op.drop_table('favorite')
    # ### end Alembic commands ###
