import re
from abc import ABC, abstractmethod
from typing import List


class Validate(ABC):

    @abstractmethod
    def validate(self):
        pass


class PersonRegisterValidate(Validate):

    def __init__(self, p_facade, username, passport):
        self.p_facade = p_facade
        self.username = username
        self.passport = passport

    def validate(self):
        if self.p_facade.get_person_by_passport(self.passport):
            raise ValueError(f"User {self.username} already exist")


class NameValidate(Validate):
    valid_username_regex = "^/[а-яёА-ЯЁ]{64}|[a-zA-Z]{64}$/u"

    def __init__(self, username: str, is_second_name=False):
        self.username = username
        self.is_second_name = is_second_name

    def validate(self):
        if self.is_second_name & self.username == None:
            pass 
        if not re.match(self.valid_username_regex, self.username):
            raise ValueError("Name should contain only letters")

class UserValidateProcess:

    def __init__(self):
        self.validation_list: List[Validate] = []
        
    def register(self, *validation: Validate):
        for el in validation:
            self.validation_list.append(el)

    def validate(self):
        for el in self.validation_list:
            el.validate()


class PassportValidate(Validate):
    valid_passport_regex = "^/[0-9]{10}$/"

    def __init__(self, passport: str):
        self.passport = passport

    def validate(self):
        if not re.match(self.valid_passport_regex, self.passport):
            raise ValueError("Wrong passport, cannot exist")
        