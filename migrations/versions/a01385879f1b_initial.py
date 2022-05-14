"""initial

Revision ID: a01385879f1b
Revises: 
Create Date: 2022-05-13 19:00:17.388011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a01385879f1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('user_access_token',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_access_token_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user_access_token'))
    )
    op.create_table('user_follower',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name=op.f('fk_user_follower_follower_id_user')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_follower_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'follower_id', name=op.f('pk_user_follower'))
    )
    op.create_table('user_privilege',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('privilege', sa.Integer(), nullable=False),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_privilege_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'privilege', name=op.f('pk_user_privilege'))
    )
    op.create_table('user_profile',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_profile_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user_profile'))
    )
    op.create_table('user_social_link_other',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(length=128), nullable=False),
    sa.Column('path', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_social_link_other_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'platform', name=op.f('pk_user_social_link_other'))
    )
    op.create_table('user_social_links',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('twitter', sa.String(length=128), nullable=True),
    sa.Column('instagram', sa.String(length=128), nullable=True),
    sa.Column('facebook', sa.String(length=128), nullable=True),
    sa.Column('reated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_social_links_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user_social_links'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_social_links')
    op.drop_table('user_social_link_other')
    op.drop_table('user_profile')
    op.drop_table('user_privilege')
    op.drop_table('user_follower')
    op.drop_table('user_access_token')
    op.drop_table('user')
    # ### end Alembic commands ###
