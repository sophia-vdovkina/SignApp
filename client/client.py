import sys
sys.path = ['', '..'] + sys.path

from preprocessing.signature_prepocessing import read_features
import os
import requests


if __name__ == "__main__":
    dir = r'.\DeepSignDB\Development\stylus'
    sig = None
    i = 0
    for file in os.listdir(dir):
        i += 1
        if i == 20:
            break
        with open(os.path.join(dir, file), 'r') as ofile:
            sig = read_features(ofile)
            json = {'signature': sig, 'name': "Sally"}
            requests.post('http://127.0.0.1:5000/api/v1/test/hello', json=json)