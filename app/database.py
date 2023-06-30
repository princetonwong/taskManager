from sqlmodel import Session, create_engine, SQLModel
from .helper import Helper as h
from sqlalchemy.orm import sessionmaker
import logging

POSTGRES_STRING = f"postgresql+psycopg2://{h.getEnv('POSTGRES_USER')}:" \
                  f"{h.getEnv('POSTGRES_PASSWORD')}@{h.getEnv('POSTGRES_HOST')}:" \
                  f"{h.getEnv('POSTGRES_PORT')}/{h.getEnv('POSTGRES_DB')}"


@h.singleton
class Database:
    def __init__(self, postgres_string=POSTGRES_STRING):
        self.POSTGRES_STRING = postgres_string
        self.engine = create_engine(self.POSTGRES_STRING,
                                    pool_size=8,
                                    echo=False,
                                    future=False)
        self.session = sessionmaker(bind=self.engine)()

    def getEngine(self):
        return self.engine

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
            logging.info(f"Connecting to DB: {self.POSTGRES_STRING}")
            logging.info(f"DB connected. Tables are: {result.all()}")
            return result.all()
