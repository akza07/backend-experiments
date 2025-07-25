from config import ENV
from sqlmodel import create_engine, SQLModel, Session

SQLITE_FILE_NAME = ENV.database_name
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

connect_args = {
    "check_same_thread": False,
}

engine = create_engine(SQLITE_URL, connect_args=connect_args)

def create_db_and_tables():
    import models  # noqa: F401
    SQLModel.metadata.create_all(bind=engine)

def flush_everything():
    import models  # noqa: F401
    SQLModel.metadata.drop_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session

