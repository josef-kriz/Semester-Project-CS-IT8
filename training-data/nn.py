from config import Config
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import precision_recall_fscore_support
from keras.models import Sequential
from keras.layers import Dense, InputLayer
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from src.classification_data_tools import limit_negative_samples
import pickle

cfg = Config()


def FetchData(cfg):
    with open(cfg.FILE, 'rb') as f:
        data = pickle.load(f)

        if cfg.SHUFFLE:
            features, targets = shuffle(data[0], data[1])

        training_features = features[:int(len(data[0]) * cfg.TRAINING_CUT) - 1]
        training_targets = targets[:int(len(data[1]) * cfg.TRAINING_CUT) - 1]
        test_features = features[int(len(data[0]) * cfg.TRAINING_CUT):]
        test_targets = targets[int(len(data[1]) * cfg.TRAINING_CUT):]

        training_features, training_targets = limit_negative_samples(training_features, training_targets, 1000)

    return training_features, training_targets, test_features, test_targets

def BuildModel(cfg, input_shape):
    model = Sequential()

    model.add(InputLayer(input_shape))

    for layer in cfg.HIDDEN_LAYERS:
        model.add(Dense(layer, use_bias=cfg.BIAS, activation=cfg.ACTIVATION_FUNCTION))

    model.add(Dense(1, use_bias=cfg.BIAS, activation='sigmoid'))

    model.compile(loss=cfg.LOSS, optimizer=cfg.OPTIMIZER, metrics=['accuracy'])

    return model

def TrainModel(cfg, model, training_features, training_targets):

    model.fit(training_features, training_targets, epochs=cfg.EPOCHS, batch_size=cfg.BATCH_SIZE, verbose=1,
                   validation_split=1 - cfg.TRAINING_CUT)

    return model

def EvaluateModel(cfg, model, test_features, test_targets):
    #predictions = model.predict(test_features)

    estimator = KerasClassifier(build_fn=model, epochs=4, batch_size=32, verbose=1)
    kfold = StratifiedKFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, test_features, test_targets, cv=kfold)
    print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))


training_X, training_y, test_X, test_Y = FetchData(cfg)

training_features = np.array(training_X)
training_targets = np.array(training_y)
test_features = np.array(test_X)
test_targets = np.array(test_Y)

input_shape = (len(training_features[0]),)

model = BuildModel(cfg, input_shape)
model = TrainModel(cfg, model, training_features, training_targets)
EvaluateModel(cfg, model, test_features, test_targets)




