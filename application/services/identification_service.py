from application.services.db_services import DBExtractor
from sklearn.model_selection import train_test_split
from sklearn import preprocessing


class Identification:

    def __init__(self):
        pass

    def train(self):
        data = DBExtractor().extract_feature_person()
                # uid -> labels
        le = preprocessing.LabelEncoder()
        le.fit(data.person_id)
        data.person_id = le.transform(data.person_id)

        X, y = self.create_Xy(data)
        X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)
        X_train,X_test,y_train,y_test = np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

        from tpot import TPOTClassifier

        # create & fit TPOT classifier with 
        tpot = TPOTClassifier(generations=100, population_size=10, scoring="balanced_accuracy",  periodic_checkpoint_folder="tpot.txt", cv=5,
                            verbosity=2, early_stop=5)
        tpot.fit(X_train, y_train)

        import timeit
        times = []
        scores = []
        winning_pipes = []
        # save our model code
        for x in range(3):
            start_time = timeit.default_timer()
            tpot.fit(X_train, y_train)
            elapsed = timeit.default_timer() - start_time
            times.append(elapsed)
            winning_pipes.append(tpot.fitted_pipeline_)
            scores.append(tpot.score(X_test, y_test))
            tpot.export('tpot_pipeline.py')
        times = [time/60 for time in times]
        print('Times:', times)
        print('Scores:', scores)   
        print('Winning pipelines:', winning_pipes)

    def return_flatten(points):
        x = []
        for point in points:
            x.append(np.array(point).flatten())
        return(x)

    def create_Xy(self, data):
        y = data.index.to_numpy(dtype="int")
        X = []
        gen = data.drop(columns=['index']).to_numpy()
        for sign in gen:
            el = []
            for feature in sign:
                el.append(feature)
            X.append(el)
        X = np.array(X)
        return X, y