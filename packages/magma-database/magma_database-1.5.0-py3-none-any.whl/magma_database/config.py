import os
from dotenv import dotenv_values
from playhouse.migrate import *


_magma_user_dir: str = os.path.join(os.path.expanduser('~'), '.magma')
os.makedirs(_magma_user_dir, exist_ok=True)

_default_config = {
    'TYPE': 'local',
    'DEBUG': True,
    'DATABASE_DRIVER': 'sqlite',
    'DATABASE_LOCATION': _magma_user_dir,
    'MYSQL_HOST': '127.0.0.1',
    'MYSQL_PORT': 3306,
    'MYSQL_DATABASE': 'seismic',
    'MYSQL_USERNAME': 'homestead',
    'MYSQL_PASSWORD': 'secret',
    'WINSTON_URL': '172.16.1.220',
    'WINSTON_PORT': 16032,
}


def env_local(filename: str = '.env.local') -> str:
    """Local environment variables set in .env.local file.

    Args:
        filename (str, optional): Environment variable name. Defaults to '.env.local'.

    Returns:
        str: Environment location
    """
    _env_local = os.path.join(os.getcwd(), filename)
    return _env_local


def env(filename: str = '.env'):
    """Production environment variables set in .env file.

    Args:
        filename (str, optional): Environment variable name. Defaults to '.env'.

    Returns:
        str: Environment location
    """
    _env = os.path.join(os.getcwd(), filename)
    return _env


def sqlite(db_name: str = 'magma.db') -> str:
    """Database location

    Args:
        db_name: database name. Default magma.db

    Returns:
        str: Database location
    """
    if os.path.isfile(DATABASE_LOCATION):
        return DATABASE_LOCATION

    if not os.path.isdir(DATABASE_LOCATION):
        os.makedirs(DATABASE_LOCATION)
    return os.path.join(DATABASE_LOCATION, db_name)


def database():
    """Database initialization"""
    _db = MySQLDatabase(host=config['MYSQL_HOST'],
                        port=int(config['MYSQL_PORT']),
                        database=config['MYSQL_DATABASE'],
                        user=config['MYSQL_USERNAME'],
                        password=config['MYSQL_PASSWORD'])

    if DATABASE_DRIVER == 'sqlite':
        sqlite_db = sqlite()

        _db = SqliteDatabase(database=sqlite_db, pragmas={
            'foreign_keys': 1,
            'journal_mode': 'wal',
            'cache_size': -32 * 1000
        })

    return _db


config = {
    **_default_config,
    **dotenv_values(env_local()),
    **dotenv_values(env())
}


DATABASE_DRIVER = config['DATABASE_DRIVER']
DATABASE_LOCATION = config['DATABASE_LOCATION']
db = database()


class Config:
    default = config
    local = dotenv_values(env_local())
    production = dotenv_values(env())

    def __repr__(self):
        return f'{self.__class__.__name__}({self.default})'
