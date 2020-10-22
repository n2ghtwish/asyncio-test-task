import click
import aiopg.sa
import att.requests as r
from aiohttp import web


async def setup_db(app):
    engine = await aiopg.sa.create_engine(dsn=app['db_url'])
    app['db'] = engine


async def close_db(app):
    engine = app['db']
    engine.close()
    await engine.wait_closed()


@click.command()
@click.option('--db-url')
@click.option('--listen')
def main(db_url, listen):
    app = web.Application()
    app['db_url'] = db_url
    app.on_startup.append(setup_db)
    app.on_cleanup.append(close_db)

    app.add_routes([
        web.post('/login', r.login),
        web.get('/user/{id}/groups', r.user_groups),
    ])

    if listen is None:
        host = 'localhost'
        port = 8000
    else:
        host_port = listen.split(':')
        host = host_port[0]
        port = int(host_port[1])

    web.run_app(app, host=host, port=port)
