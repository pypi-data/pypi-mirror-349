import os
import datetime
import shutil
from .config import DATABASE_DRIVER, DATABASE_LOCATION, database, sqlite, db
from .models.volcano import Volcano
from .models.station import Station
from .models.sds import Sds
from .models.rsam_csv import RsamCSV
from .models.winston_scnl import WinstonSCNL
from .models.mounts import MountsSO2, MountsThermal
from playhouse.migrate import *

MODELS = [Volcano, Station, Sds, RsamCSV, WinstonSCNL, MountsSO2, MountsThermal]


def test() -> bool:
    """Test database connection.

    Returns:
        bool: True if database connection is successful, False otherwise.
    """
    db_proxy = DatabaseProxy()
    _db = database()

    try:
        print('🏃‍♂️ Checking database connection...')
        print(f'➡️ Using {DATABASE_DRIVER}')
        db_proxy.initialize(_db)
        _db.connect()
        _db.close()
        print('✅ Database connection successful.')
        return True
    except Exception as e:
        print(f"❌ Cannot connect to database: {e}")
        return False


def init(verbose: bool = True) -> bool:
    """Initialize the database."""
    try:
        migrate(reset=False, verbose=verbose)
        Volcano.fill_database()
        WinstonSCNL.fill_database()
        if verbose:
            print('Database initialized.')
        return True
    except Exception as e:
        if verbose:
            print(f'❌ Database initialization error: {e}')
        return False


def migrate(reset: bool = False, verbose: bool = True) -> bool | None:
    """Reset database.

    Returns:
        True | None
    """
    if DATABASE_DRIVER == 'sqlite':
        database_location = sqlite(DATABASE_LOCATION)
        if os.path.exists(database_location) and reset:
            if not db.is_closed():
                db.close()

            os.remove(database_location)
            db.connect(reuse_if_open=True)
            db.create_tables(MODELS)
            db.close()
            if verbose:
                print(f"⌛ Migrate database: {database_location}")
            return True

    if DATABASE_DRIVER == 'mysql':
        db.connect(reuse_if_open=True)
        db.drop_tables(MODELS)
        db.create_tables(MODELS)
        db.close()

    Volcano.fill_database()
    if verbose:
        print('✅ Finishing Migrating')

    return None


def backup(backup_dir: str = None) -> str | None:
    """Backup database before run

    Args:
        backup_dir: directory to back up

    Returns:
        str: backup file location
    """
    if DATABASE_DRIVER == 'sqlite':
        print("Backing up SQlite database...")
        source_database = sqlite()
        source_filename = os.path.basename(source_database)

        if backup_dir is None:
            backup_dir = os.path.dirname(source_database)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{source_filename}-{timestamp}.bak"

        backup_database = os.path.join(backup_dir, backup_filename)
        shutil.copy(source_database, backup_database)
        print(f"Backup database saved to: {backup_database}")
        return backup_database

    print('For now, only sqlite backup is supported.')
