from abc import ABC, abstractmethod
from application.models import ReferenceParams
from application.services.validate_service import UserValidateProcess, NameValidate, PersonRegisterValidate, PassportValidate
from application.facades.db_facades import DeviceFacade, PersonFacade, InfoFacade, ReferenceParamsFacade, SignatureFacade, SignatureSetFacade, FeatureFacade
from application.services.create_db_records import PersonCreator, InfoCreator, DeviceCreator, SigSetCreator, SignatureCreator
import json

class RegistrationStrategy(ABC):
    @abstractmethod
    def register(self):
        pass


class PersonRegistrationService(RegistrationStrategy):

    def __init__(self, json):
        self.json      = json
        self.p_facade  = PersonFacade()

    def register(self):
        data = self.json
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

        info_register_context = InformationService(user.id, data)
        code = info_register_context.register()
        return 200, {
            "message"       : f'User {user.name} {user.surname} was registered',
        }


class InformationService(RegistrationStrategy):

    def __init__(self, user, json):
        self.json      = json
        self.user = user
        self.i_facade = InfoFacade()

    def register(self):
        data = self.json
        info = InfoCreator(self.i_facade, self.user, data).create()
        return 200


class SignatureRegistrationService(RegistrationStrategy):

    def __init__(self, json):
        self.json      = json
        self.sig_s_facade = SignatureSetFacade()
        self.dev_facade = DeviceFacade() 
        self.sig_facade = SignatureFacade()
        self.feat_facade = FeatureFacade()

    def register(self):
        data = self.json
        user = PersonFacade().get_person_by_passport(data['passport'])
        device = DeviceCreator(self.dev_facade, data).create()
        set = SigSetCreator(self.sig_s_facade, user.id, data['set_isActive']).create()
        for sig in data['signatures']:
            SignatureCreator(self.sig_facade, self.feat_facade, set.id, device.id, sig).create()
        return 200