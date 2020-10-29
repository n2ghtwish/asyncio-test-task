import sqlalchemy as sa
from aiohttp import web
from att.db.schema import t_user

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
