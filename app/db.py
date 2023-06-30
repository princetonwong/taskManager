from sqlmodel import Session, create_engine, SQLModel
from .helper import Helper as h
from sqlalchemy.orm import sessionmaker
import logging


@h.singleton
class Database:
    def __init__(self):
        self.POSTGRES_STRING = f"postgresql+psycopg2://{h.getEnv('POSTGRES_USER')}:{h.getEnv('POSTGRES_PASSWORD')}@{h.getEnv('POSTGRES_HOST')}:{h.getEnv('POSTGRES_PORT')}/{h.getEnv('POSTGRES_DB')}"
        self.engine = create_engine(self.POSTGRES_STRING,
                                    pool_size=8,
                                    echo=False,
                                    future=False)
        self.session = sessionmaker(bind=self.engine)()

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)

    def getSession(self):
        with Session(self.engine) as session:
            yield session

    def executeQuery(self, query):
        with Session(self.engine) as session:
            session.execute(query)
            session.commit()

    def listAllTables(self):
        with Session(self.engine) as session:
            result = session.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """)
            logging.info(f"DB connected. Tables are: {result.all()}")
            return result
