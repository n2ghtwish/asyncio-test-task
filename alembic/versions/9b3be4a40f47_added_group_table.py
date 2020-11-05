"""Added group table

Revision ID: 9b3be4a40f47
Revises: af1a150d0ff2
Create Date: 2020-11-02 23:55:06.170787

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from att.db.schema import t_user

# revision identifiers, used by Alembic.
revision = '9b3be4a40f47'
down_revision = 'af1a150d0ff2'
branch_labels = None
depends_on = None


def upgrade():
    groups = op.create_table('groups',
                             sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                                       nullable=False),
                             sa.Column('name', sa.String(), nullable=False),
                             sa.CheckConstraint('length(name) > 0', name=op.f('ck_groups_name_len_gt_0')),
                             sa.PrimaryKeyConstraint('id', name=op.f('pk_groups')),
                             schema='core'
                             )
    op.create_table('user_groups',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'),
                              nullable=False),
                    sa.Column('user_id', sa.ForeignKey(t_user.c.id), nullable=False),
                    sa.Column('group_id', sa.ForeignKey(groups.c.id), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_groups')),
                    schema='core'
                    )


def downgrade():
    op.drop_table('user_groups', schema='core')
    op.drop_table('groups', schema='core')
