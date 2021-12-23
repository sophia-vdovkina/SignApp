from application.database import db_session, engine
from application import models
from application.facades.abstract_facade import AbstractFacade


class PersonFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Person)

    def get_person_by_passport(self, passport: str):
        return models.Person.query.filter_by(passport=passport).first()

class ReferenceParamsFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.ReferenceParams)


class SecuritySettingsFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.SecuritySettings)


class InfoFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Info)


class SignatureSetFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.SignatureSet)


class SignatureFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Signature)


class DeviceFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Device)


class FeatureFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Feature)


class LoginAttempts(AbstractFacade):

    def __init__(self):
        super().__init__(models.LoginAttempts)


class IdentificationAttempts(AbstractFacade):

    def __init__(self):
        super().__init__(models.IdentificationAttempts)

