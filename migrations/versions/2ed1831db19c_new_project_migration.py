"""new project migration

Revision ID: 2ed1831db19c
Revises: 
Create Date: 2024-06-15 22:14:23.236720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ed1831db19c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('art_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bank_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_holder_name', sa.String(length=100), nullable=False),
    sa.Column('account_number', sa.String(length=20), nullable=False),
    sa.Column('routing_number', sa.String(length=9), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('art_subtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subtype_name', sa.String(length=50), nullable=False),
    sa.Column('art_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['art_type_id'], ['art_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('street_address', sa.String(length=100), nullable=False),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('youtube_link', sa.String(length=120), nullable=True),
    sa.Column('instagram_link', sa.String(length=120), nullable=True),
    sa.Column('bank_account_id', sa.Integer(), nullable=True),
    sa.Column('art_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['art_type_id'], ['art_type.id'], ),
    sa.ForeignKeyConstraint(['bank_account_id'], ['bank_account.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('art_subtype')
    op.drop_table('bank_account')
    op.drop_table('art_type')
    # ### end Alembic commands ###
