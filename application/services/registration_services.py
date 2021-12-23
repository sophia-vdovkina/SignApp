from abc import ABC, abstractmethod
from application.services.validate_service import UserValidateProcess, NameValidate, PersonRegisterValidate, PassportValidate
from application.facades.db_facades import PersonFacade, InfoFacade
from application.services.create_db_records import Creator, PersonCreator
import json

class RegistrationStrategy(ABC):
    @abstractmethod
    def registrate(self):
        pass


class PersonRegistrationService(RegistrationStrategy):

    def __init__(self, json):
        self.json      = json
        self.p_facade  = PersonFacade()
        self.i_facade = InfoFacade()

    def registrate(self):
        data = json.loads(self.json)
        validate_user = UserValidateProcess()
        validate_user.register(
            NameValidate(data['name']),
            NameValidate(data['second_name'], True),
            NameValidate(data['surname']),
            PassportValidate(data['passport']),
            PersonRegisterValidate(self.p_facade, data['name']+' '+data['surname'], data['passport'])
        )

        try:
            validate_user.validate()
        except ValueError as ex:
            return 400, {"error": str(ex)}

        user = PersonCreator(self.p_facade, data).create()

        return 200, {
            "message"       : f'User {user.name} {user.surname} was registred',
        }