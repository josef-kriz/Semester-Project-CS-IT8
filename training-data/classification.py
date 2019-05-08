from src.classification_print_tools import print_graph_graphviz, print_data_statistics, \
    print_prediction_statistics, draw_roc_curve_plotlib
from sklearn.utils import shuffle
from sklearn import tree
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn import linear_model
import matplotlib.pyplot as plt
import pickle

# CONFIG
training_test_ratio = 0.7
negative_samples_ratio = 800
shuffle_data = True
print_graph = False
draw_roc_curve = True
file_name = 'output/training-full.pickle'


def limit_negative_samples(features, targets, negative_count):
    limited_features = []
    limited_targets = []
    for i in range(0, len(targets)):
        if targets[i] == 1 or negative_count > 0:
            limited_features.append(features[i])
            limited_targets.append(targets[i])
        if targets[i] == 0:
            negative_count -= 1
    return limited_features, limited_targets


def split_data(features, targets, training_ratio, neg_limit=False, print_stats=True):
    boundary_index = int(len(features) * training_ratio)

    training_data = [
        features[:boundary_index],
        targets[:boundary_index]
    ]

    if neg_limit != False:
        training_data[0],  training_data[1] = limit_negative_samples(training_data[0], training_data[1], neg_limit)

    test_data = [
        features[boundary_index:],
        targets[boundary_index:]
    ]

    if print_stats:
        print_data_statistics(training_data, test_data)

    return training_data, test_data


with open(file_name, 'rb') as f:
    data = pickle.load(f)

features = data[0]
targets = data[1]

if shuffle_data:
    features, targets = shuffle(features, targets)

for [limit, color] in [[600, 'blue'], [700, 'darkorange'], [2000, 'red'], [10000, 'brown'], [90000, 'green']]:
    train_data, test_data = split_data(features, targets, training_test_ratio, limit)
    clf = ensemble.RandomForestClassifier()
    # clf = neighbors.KNeighborsClassifier(n_neighbors=4)
    # clf = tree.DecisionTreeClassifier()
    # clf = linear_model.LogisticRegression()
    clf = clf.fit(train_data[0], train_data[1])

    predictions = clf.predict(test_data[0])

    print_prediction_statistics(predictions, test_data, limit)

    if draw_roc_curve:
        draw_roc_curve_plotlib(test_data[1], predictions, limit, color)

    if print_graph:
        print_graph_graphviz(clf)

plt.show()





