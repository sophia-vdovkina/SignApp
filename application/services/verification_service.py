import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from itertools import combinations

from application.services.db_services import DBExtractor
from application.facades.db_facades import ReferenceParamsFacade, SecuritySettingsFacade, LoginAttempts, SignatureFacade, FeatureFacade, DeviceFacade, PersonFacade
from application.services.create_db_records import ParamsCreator, VerificationAttemptsCreator, SignatureCreator, DeviceCreator


class VerificationService:

    def __init__(self) -> None:
        self.extracter = DBExtractor()
        self.sig_facade = SignatureFacade()
        self.feat_facade = FeatureFacade()
        self.p_facade = ReferenceParamsFacade()
        self.s_facade = SecuritySettingsFacade()
        self.v_facade = LoginAttempts()

    def train(self):
        # data = self.extracter.extract_feature_person()
        data = pd.read_pickle("data.pkl")
        X = data.drop(columns=['index', 'person_id']).values
        y = data.person_id.to_numpy()
        pca_X = []
        pca = PCA(n_components = 2)
        index = y[0]

        for i in range(len(X)):

            if index != y[i]:
                lengths = []
                for combo in combinations(pca_X, 2):
                    lengths.append(self.dtw(np.array(combo[0]).flatten(), np.array(combo[1]).flatten(), 1))

                self.put_in_DB(max(lengths), np.mean(lengths), min(lengths), index)
                
                index = y[i]
                pca_X = []
           
            pca_el = pca.fit_transform(self.create_X(X[i]))
            pca_X.append(pca_el)

        return 200

    # Двухфакторная аутентификация пользователя по его подписи и паролю
    def verify(self, data):
        person = PersonFacade().get_person_by_passport(data['passport'])

        # проверка введенного пароля
        # password = self.extracter.get_password(data['passport'])
        # if not password == data['password']:
        #     return 200, "Person {} {} {} is not verified".format(person.name, person.second_name, person.surname)

        # извлечение параметров для верификации подписи из базы
        params = self.extracter.get_params(data['passport'])
        vect = (params.max_value, params.mean_value, params.min_value)

        dev_facade = DeviceFacade() 
        device = DeviceCreator(dev_facade, data).create()
        # создание записи о введенной подписи в базе данных
        signature = SignatureCreator(self.sig_facade, self.feat_facade, None, device.id, data['signatures']).create()
        
        pca_X = []
        pca_template_X = []
        
        # получение параметров из введенной подписи
        features = self.extracter.get_features_by_id(signature.id)
        temp_features = self.extracter.get_features_by_person(person.id)

        template_X = temp_features.drop(columns=['index', 'person_id']).to_numpy()

        # применение метода главных компонент и верификация подписи
        pca = PCA(n_components = 2)
        pca_X = pca.fit_transform(self.create_X(features.values[0]))
        
        for i in template_X:
            pca_template_X.append(pca.fit_transform(self.create_X(i)))
            
        lengths = []
        for temp in pca_template_X:
            lengths.append(self.dtw(np.array(pca_X).flatten(), np.array(temp).flatten(), window = 1))
        res = (np.array((max(lengths), np.mean(lengths), min(lengths))) >= vect).sum() > 1

        # Занесение записи о попытке верификации в БД
        VerificationAttemptsCreator(self.v_facade, person.id, signature.id, res).create()

        if res:
            return 200, True, "Person {} {} {} verified".format(person.name, person.second_name, person.surname)
        else:
            return 200, False, "Person {} {} {} is not verified".format(person.name, person.second_name, person.surname)

    def put_in_DB(self, max, mean, min, id):
        ParamsCreator(self.p_facade, self.s_facade, {'max': max, 'mean': mean, 'min': min}, id).create()

    def create_X(self, data):
        person_features = np.zeros(shape=(7,256))
        for k,m in enumerate(data):
            person_features[k] = m

        return person_features.transpose()

    def dtw(self, s, t, window):
        n, m = len(s), len(t)
        w = np.max([window, abs(n-m)])
        dtw_matrix = np.zeros((n+1, m+1))
        
        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf
        dtw_matrix[0, 0] = 0
        
        for i in range(1, n+1):
            for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
                dtw_matrix[i, j] = 0
        
        for i in range(1, n+1):
            for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
                cost = abs(s[i-1] - t[j-1])
                # take last min from a square box
                last_min = np.min([dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[-1,-1]