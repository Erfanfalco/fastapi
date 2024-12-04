import logging
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser as cf
import urllib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Path to the INI file
CONFIG_PATH = "App/routers/Database/Setup.ini"


def load_config():
    """Load configuration from the INI file."""
    conf = cf.ConfigParser()
    conf.read(CONFIG_PATH)
    return conf


def create_sql_engine(conf):
    """Create and return an SQL Server engine."""
    try:
        username = conf.get('db_cred', 'Name')
        password_encoded = urllib.parse.quote_plus(conf.get('db_cred', 'password'))
        server = conf.get('db_cred', 'server')
        source_name = conf.get('db_cred', 'database')

        engine = create_engine(
            f'mssql+pymssql://{username}:{password_encoded}@{server}:1433/{source_name}?driver=ODBC+Driver+17+for+SQL+Server'
        )
        logger.info("Successfully connected to SQL Server.")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to SQL Server: {e}")
        raise


def create_postgres_engine(conf):
    """Create and return a PostgreSQL engine."""
    try:
        p_username = conf.get('my_db', 'user')
        p_password_encoded = conf.get('my_db', 'password')
        p_server = conf.get('my_db', 'host')
        p_source_name = conf.get('my_db', 'dbname')
        p_port = conf.get('my_db', 'port')

        postgres_path = f'postgresql+psycopg2://{p_username}:{p_password_encoded}@{p_server}:{p_port}/{p_source_name}'

        engine = create_engine(postgres_path)
        logger.info("Successfully connected to PostgreSQL.")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise


# Load configuration and create engines
config = load_config()
sql_engine = create_sql_engine(config)
postgres_engine = create_postgres_engine(config)

# SQLAlchemy session makers
SQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)
PostgresSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)


# Dependency functions
def get_sql_db_session():
    """Dependency function to get a new SQL Server DB session."""
    db = SQLSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_postgres_db_session():
    """Dependency function to get a new PostgreSQL DB session."""
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()
