import sys
import names
sys.path = ['', '..'] + sys.path

from preprocessing.signature_prepocessing import read_features
import os
import requests

json = {
        "name": "Ivan",
        "surname": "Ivanov",
        "second_name": "Ivanovich",
        "passport": "5640322252",
        "organization": "ПГУ",
        "registration_date": None,
        "comment": "hello world",
        "device_name": "stylus",
        "device_pressure": True,
        'set_isActive': True,
        'signatures': []
    }

if __name__ == "__main__":
    # dir = r'.\DeepSignDB\Development\stylus'
    # sig = None
    # name = 0
    # i = 0
    # for file in os.listdir(dir):
    #     sig = []
    #     if name != file[:5]:
    #         json["name"] = names.get_first_name()
    #         json["surname"] = names.get_last_name()
    #         json["second_name"] = names.get_first_name()
    #         json["passport"] = str(int(json["passport"])+1)
    #         if i>0:
    #             requests.post('http://127.0.0.1:5000/api/v1/test/hello', json=json)
    #             requests.post('http://127.0.0.1:5000/api/v1/test/sig', json=json)
    #             json['signatures'] = []
    #         i += 1
    #         name = file[:5]
    #     with open(os.path.join(dir, file), 'r') as ofile:
    #         sig = read_features(ofile)
    #         json['signatures'].append(sig)

    requests.post('http://127.0.0.1:5000/api/v1/test/identificate', json=json)
