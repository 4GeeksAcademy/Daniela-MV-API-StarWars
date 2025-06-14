"""empty message

Revision ID: 96b3a9fc84ce
Revises: a5cffa318ac2
Create Date: 2025-06-05 19:52:28.201422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96b3a9fc84ce'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('gender', sa.String(length=120), nullable=False),
    sa.Column('hair_color', sa.String(length=120), nullable=False),
    sa.Column('eye_color', sa.String(length=120), nullable=False),
    sa.Column('birth_year', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gender')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('climate', sa.String(length=120), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.Column('terrain', sa.String(length=120), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('model', sa.String(length=120), nullable=False),
    sa.Column('cargo_capacity', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=120), nullable=False),
    sa.Column('passengers', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('user_name', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['name'])
        batch_op.create_unique_constraint(None, ['user_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_name')
        batch_op.drop_column('name')

    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###
