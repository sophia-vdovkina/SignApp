# import sys
# sys.path = ['', '..'] + sys.path
from abc import ABC, abstractmethod
import numpy 
from application import models
from application.services.extract_features import FeatureExtracter

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


class InfoCreator(Creator):

    def __init__(self, in_facade, person, data):
        self.data = data
        self.in_facade = in_facade
        self.person = person

    def create(self):
        info = models.Info(
            person_id = self.person,
            organization = self.data["organization"],
            registration_date = self.data["registration_date"],
            comment = self.data["comment"]
        )
        self.in_facade.create(info)
        return info

class SignatureCreator(Creator):
    
    def __init__(self, s_facade, f_facade, set, device, data):
        self.s_facade = s_facade
        self.f_facade = f_facade
        self.set = set
        self.device = device
        self.data = data

    def create(self):
        signature = models.Signature(
            set_id = self.set,
            device_id = self.device
        )
        self.s_facade.create(signature)
        features = FeatureExtracter(self.data).extract()
        FeatureCreator(self.f_facade, signature.id, features).create()


class DeviceCreator(Creator):

    def __init__(self, d_facade, data):
        self.d_facade = d_facade
        self.data = data

    def create(self):
        name = self.data['device_name']
        device = self.d_facade.get_device_by_name(name)
        if device:
            return device
        device = models.Device(
            name = name,
            has_pressure = self.data["device_pressure"],
        )
        self.d_facade.create(device)
        return device

class SigSetCreator(Creator):

    def __init__(self, facade, person, isActive):
        self.facade = facade
        self.person = person,
        self.activity = isActive

    def create(self):
        set = models.SignatureSet(
            person_id = self.person,
            isActive = self.activity
        )
        self.facade.create(set)
        return set


class FeatureCreator(Creator):

    def __init__(self, facade, sig, features):
        self.facade = facade
        self.features = features
        self.sig = sig

    def create(self):
        i = 0
        for key in self.features.keys():
            feature = models.Feature(
                signature_id = self.sig,
                values = self.features[key].tolist(),
                name = str(key),
                index = i
            )
            self.facade.create(feature)
            i = i + 1
        return 200

