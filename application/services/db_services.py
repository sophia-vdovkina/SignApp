from application.facades import db_facades
from scipy import stats
import numpy as np
import pandas as pd
class DBExtractor:

    def __init__(self):
        pass

    def extract_feature_person(self):
        data = pd.DataFrame(columns=['x', 'y', 'p', 'v', 'acceleration', 'angle', 'radius', 'person_id'])
        row = pd.Series()
        people = db_facades.PersonFacade().get_all()
        for person in people:
            id = person.id
            row['person_id'] = id
            for set in person.signature_sets:
                if set.isActive:
                    for signature in set.signature:
                        for feature in signature.features:
                            values = feature.values
                            # normalization and interpolation
                            val = stats.zscore(np.interp(np.arange(0, len(values),  len(values)/256), np.arange(0, len(values)), values))
                            name = feature.name
                            row[name] = val        
                        data.append(row,ignore_index=True)
        return data