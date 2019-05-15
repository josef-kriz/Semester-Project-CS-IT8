from config import Config
import numpy as np
from itertools import product
from sklearn.utils import shuffle
from sklearn.metrics import precision_recall_fscore_support
from keras import callbacks
from keras.models import Sequential
from keras.layers import Dense, InputLayer
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from src.classification_data_tools import limit_negative_samples
import pickle

np.random.seed(7)
cfg = Config()



def FetchData(cfg):
    with open(cfg.FILE, 'rb') as f:
        data = pickle.load(f)

        if cfg.SHUFFLE:
            features, targets = shuffle(data[0], data[1])
        else:
            features = data[0]
            targets = data[1]

        training_features = features[:int(len(data[0]) * cfg.TRAINING_CUT) - 1]
        training_targets = targets[:int(len(data[1]) * cfg.TRAINING_CUT) - 1]
        test_features = features[int(len(data[0]) * cfg.TRAINING_CUT):]
        test_targets = targets[int(len(data[1]) * cfg.TRAINING_CUT):]

        if cfg.NEGATIVE_SAMPLES_RATIO != 0:
            training_features, training_targets = limit_negative_samples(training_features, training_targets, cfg.NEGATIVE_SAMPLES_RATIO)

    return training_features, training_targets, test_features, test_targets

def BuildModel(cfg, input_shape, iftest, hidden_layers):
    model = Sequential()

    model.add(InputLayer(input_shape))

    if iftest:
        for layer in hidden_layers:
            model.add(Dense(layer, use_bias=cfg.BIAS, activation=cfg.ACTIVATION_FUNCTION))
    else:
        for layer in cfg.HIDDEN_LAYERS:
            model.add(Dense(layer, use_bias=cfg.BIAS, activation=cfg.ACTIVATION_FUNCTION))

    model.add(Dense(1, use_bias=cfg.BIAS, activation='sigmoid'))

    model.compile(loss=cfg.LOSS, optimizer=cfg.OPTIMIZER, metrics=['accuracy'])

    return model

def TrainModel(cfg, model, training_features, training_targets):
    if cfg.EARLY_STOPPING:
        es = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=cfg.EARLY_STOPPING_PATIENCE, verbose=0, mode='min')

        model.fit(training_features, training_targets, epochs=cfg.EPOCHS, callbacks=[es], class_weight=cfg.CLASS_WEIGHT, batch_size=cfg.BATCH_SIZE, verbose=1,
                        validation_split=1 - cfg.TRAINING_CUT)
    else:
        model.fit(training_features, training_targets, epochs=cfg.EPOCHS, class_weight=cfg.CLASS_WEIGHT,
                  batch_size=cfg.BATCH_SIZE, verbose=1,
                  validation_split=1 - cfg.TRAINING_CUT)

    return model

def EvaluateModel(cfg, model, test_features, test_targets):
    predictions = model.predict(test_features)

    for prediction in predictions:
        if prediction[0] < 0.5:
            prediction[0] = 0
        else:
            prediction[0] = 1

    print(precision_recall_fscore_support(test_targets, predictions, average='macro'))

def EvaluateModelTest(cfg, model, test_features, test_targets):
    predictions = model.predict(test_features)

    for prediction in predictions:
        if prediction[0] < 0.5:
            prediction[0] = 0
        else:
            prediction[0] = 1

    return precision_recall_fscore_support(test_targets, predictions, average='macro')

    #estimator = KerasClassifier(build_fn=model, epochs=4, batch_size=32, verbose=1)
    #kfold = StratifiedKFold(n_splits=10, shuffle=True)
    #results = cross_val_score(estimator, test_features, test_targets, cv=kfold)
    #print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))


training_X, training_y, test_X, test_Y = FetchData(cfg)

training_features = np.array(training_X)
training_targets = np.array(training_y)
test_features = np.array(test_X)
test_targets = np.array(test_Y)

input_shape = (len(training_features[0]),)

if cfg.MULTIPLE_ARCHITECTURES:
    best_architecture = []
    best_precision = 0
    best_recall = 0
    best_f1 = 0
    count_max = 0
    counter = 0

    architecture_list = []

    for i in range(2, cfg.TEST_LAYERS + 1):
        prod = list(product(cfg.TEST_NOTES, repeat = i))
        architecture_list.extend(prod)

    count_max = len(architecture_list)

    for architecture in architecture_list:
        print(str(counter) + '/' + str(count_max))

        model = BuildModel(cfg, input_shape, True, list(architecture))
        model = TrainModel(cfg, model, training_features, training_targets)
        precision, recall, f1, none = EvaluateModelTest(cfg, model, test_features, test_targets)

        if f1 > best_f1:
            best_precision = precision
            best_recall = recall
            best_f1 = f1
            best_architecture = list(architecture)

        counter += 1

    print('BEST ARCHITECTURE:')
    print(best_architecture)
    print('precision: ' + str(best_precision) + ', recall: ' + str(best_recall) + ', f1: ' + str(best_f1))


else:
    model = BuildModel(cfg, input_shape, False, 0)
    model = TrainModel(cfg, model, training_features, training_targets)
    EvaluateModel(cfg, model, test_features, test_targets)




