import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def run_sql(statements):
    conn = psycopg2.connect(
        dbname  =os.getenv("POSTGRES_DB"),
        user    =os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host    =os.getenv("POSTGRES_HOSTNAME"),
        port    =os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()