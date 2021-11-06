import psycopg2
import os
from env import env
from abc import ABC, abstractmethod
from managment.utils import run_sql

class ConsoleCommand(ABC):
    """
    Интерфейс Консольной команды для ее выполнения
    """

    @abstractmethod
    def execute(self):
        pass


class InitialDBCommand(ConsoleCommand):
    """
    Команда инициализации базы данных
    """
    
    def execute(self):
        env.configure_app()

        try:
            run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
        except psycopg2.errors.lookup('42P04'):
            print(
                f"Databse {os.getenv('APPLICATION_DB')} already exist and will not be recreated"
            )
