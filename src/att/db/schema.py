import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


CORE_SCHEMA = 'core'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = sa.MetaData(
    schema=CORE_SCHEMA,
    naming_convention=convention
)

t_user = sa.Table(
    'user', metadata,
    sa.Column('id', pg.UUID(as_uuid=True), primary_key=True,
              server_default=sa.func.gen_random_uuid()),
    sa.Column('login', sa.String, nullable=False),
    sa.Column('password', sa.String, nullable=False),
    sa.CheckConstraint('length(login) > 0', name='login_len_gt_0'),
    sa.CheckConstraint('lower(login) = login', name='login_is_lowercase'),
    sa.CheckConstraint('length(password) > 0', name='password_len_gt_0'),
)

t_groups = sa.Table(
    'groups', metadata,
    sa.Column('id', pg.UUID(as_uuid=True), primary_key=True,
              server_default=sa.func.gen_random_uuid()),
    sa.Column('name', sa.String, nullable=False),
    sa.CheckConstraint('length(name) > 0', name='name_len_gt_0'),
)

t_user_groups = sa.Table(
    'user_groups', metadata,
    sa.Column('id', pg.UUID(as_uuid=True), primary_key=True,
              server_default=sa.func.gen_random_uuid()),
    sa.Column('user_id', sa.ForeignKey(t_user.columns.id), nullable=False),
    sa.Column('group_id', sa.ForeignKey(t_groups.columns.id), nullable=False)
)
