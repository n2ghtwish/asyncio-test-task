import sqlalchemy as sa
from aiohttp import web
from att.db.schema import t_user, t_groups, t_user_groups

CHECK_PASSWORD = (
    sa.select([
        t_user.c.id.label('user_id'),
    ])
    .where(t_user.c.login == sa.bindparam('login'))
    .where(t_user.c.password == sa.func.crypt(sa.bindparam('password'), t_user.c.password))
)

CHECK_USER = (
    sa.select([
        t_user.c.id.label('user_id'),
    ])
    .where(t_user.c.login == sa.bindparam('login'))
)

ADD_USER = (
    sa.insert(t_user)
    .values([{'login': sa.bindparam('login'),
              'password': sa.func.crypt(sa.bindparam('password'), sa.func.gen_salt('bf', 8))}])
    .returning(t_user.c.id.label('user_id'))
)

CHECK_GROUP = (
    sa.select([
        t_groups.c.id.label('group_id'),
    ])
    .where(t_groups.c.name == sa.bindparam('group'))
)

ADD_GROUP = (
    sa.insert(t_groups)
    .values([{'name': sa.bindparam('group')}])
    .returning(t_groups.c.id.label('group_id'))
)

CHECK_USER_GROUP = (
    sa.select([
        t_user_groups.c.id.label('record_id'),
    ])
    .where(t_user_groups.c.user_id == sa.bindparam('user'))
    .where(t_user_groups.c.group_id == sa.bindparam('group'))
)

ADD_USER_GROUP = (
    sa.insert(t_user_groups)
    .values([{'user_id': sa.bindparam('user'),
              'group_id': sa.bindparam('group')}])
    .returning(t_user_groups.c.id.label('record_id'))
)

REMOVE_USER_GROUP = (
    sa.delete(t_user_groups)
    .where(t_user_groups.c.id == sa.bindparam('id'))
)


def make_login_response(user_id):
    if user_id is not None:
        return web.json_response({'user_id': str(user_id)})
    else:
        return web.json_response({'error': 'auth failed'})


async def login(request):
    params = await request.json()
    login = params.get('login')
    password = params.get('password')

    async with request.app['db'].acquire() as conn:
        result = await conn.execute(
            CHECK_PASSWORD, login=login, password=password
        )
        user_id = await result.scalar()

    return make_login_response(user_id)


async def user_groups(request):
    user_id = request.match_info.get('id', None)
    groups = []

    # fill the gap

    return web.json_response({'groups': groups})


async def signup(request):
    params = await request.json()
    login = params.get('login')
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(CHECK_USER, login=login)
        user_id = await result.scalar()
        if user_id is None:
            password = params.get('password')
            result = await conn.execute(ADD_USER, login=login, password=password)
            user_id = await result.scalar()
            return web.json_response({'user_id': str(user_id)})
        else:
            return web.json_response({'error': 'user already exists'})


async def group(request):
    params = await request.json()
    group_name = params.get('group')
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(CHECK_GROUP, group=group_name)
        group_id = await result.scalar()
        if group_id is None:
            result = await conn.execute(ADD_GROUP, group=group_name)
            group_id = await result.scalar()
            return web.json_response({'group_id': str(group_id)})
        else:
            return web.json_response({'error': 'group already exists'})


async def add_to_group(request):
    params = await request.json()
    login = params.get('login')
    group_name = params.get('group')
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(CHECK_USER, login=login)
        user_id = await result.scalar()
        if user_id is None:
            return web.json_response({'error': 'user not found'})
        else:
            result = await conn.execute(CHECK_GROUP, group=group_name)
            group_id = await result.scalar()
            if group_id is None:
                return web.json_response({'error': 'group not found'})
            else:
                result = await conn.execute(CHECK_USER_GROUP, user=user_id, group=group_id)
                record_id = await result.scalar()
                if record_id is None:
                    result = await conn.execute(ADD_USER_GROUP, user=user_id, group=group_id)
                    record_id = await result.scalar()
                    return web.json_response({'success': str(record_id)})
                else:
                    return web.json_response({'error': 'user already in this group'})


async def remove_from_group(request):
    params = await request.json()
    login = params.get('login')
    group_name = params.get('group')
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(CHECK_USER, login=login)
        user_id = await result.scalar()
        if user_id is None:
            return web.json_response({'error': 'user not found'})
        else:
            result = await conn.execute(CHECK_GROUP, group=group_name)
            group_id = await result.scalar()
            if group_id is None:
                return web.json_response({'error': 'group not found'})
            else:
                result = await conn.execute(CHECK_USER_GROUP, user=user_id, group=group_id)
                record_id = await result.scalar()
                if record_id is not None:
                    await conn.execute(REMOVE_USER_GROUP, id=record_id)
                    return web.json_response({'success': f'removed user {login} from group {group_name}'})
                else:
                    return web.json_response({'error': 'user is not in group'})
