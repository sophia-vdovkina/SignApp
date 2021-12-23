# import sys
# sys.path = ['', '..'] + sys.path
from abc import ABC, abstractmethod
from application import models
from application.facades import db_facades


class Creator(ABC):
    """
    Abstract create records of datasets based on ther json
    """

    @abstractmethod
    def create(self):
        pass


class PersonCreator(Creator):

    def __init__(self, p_facade, data):
        self.data = data
        self.p_facade = p_facade
    
    def create_user(self):
        new_person = models.Person(
            name = self.data["name"],
            surname = self.data["surname"],
            second_name = self.data["second_name"],
            passport = self.data["passport"]
        )
        return new_person

    def create(self):
        user = self.create_user()
        self.p_facade.create(user)
        return user
