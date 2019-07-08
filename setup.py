from setuptools import setup, find_packages

setup(
    name='att',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click',
        'aiopg',
        'psycopg2-binary',
        'sqlalchemy',
        'alembic',
        'aiohttp',
        'jinja2',
        'asyncio_extras',
        'async_timeout',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-asyncio',
            'pytest-mock',
        ]
    },
    entry_points='''
    [console_scripts]
    att-server=att.server:main
    ''',
)
