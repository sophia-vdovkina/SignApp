from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from application.config import Config

db_session = None
engine = None
Base = None

def setup_db():
    global db_session, engine, Base

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
                                            
    Base = declarative_base()
    Base.query = db_session.query_property()