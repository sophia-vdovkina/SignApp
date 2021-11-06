import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["APPLICATION_DB"]

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    pass