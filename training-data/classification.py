from src.classification_print_tools import print_graph_graphviz, print_data_statistics, draw_roc_curve_plotlib
from src.classification_data_tools import split_data
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
shuffle_data = False
print_graph = False
draw_roc_curve = True
file_name = 'output/training-full-shuffled.pickle'


with open(file_name, 'rb') as f:
    data = pickle.load(f)

features = data[0]
targets = data[1]

# if shuffle_data:
#     features, targets = shuffle(features, targets)

for [limit, color] in [[600, 'blue'], [700, 'darkorange'], [2000, 'red'], [10000, 'brown']]:
    train_data, test_data = split_data(features, targets, training_test_ratio, limit)
    # clf = ensemble.RandomForestClassifier()
    # clf = neighbors.KNeighborsClassifier(n_neighbors=4)
    # clf = tree.DecisionTreeClassifier()
    clf = linear_model.LogisticRegression(solver='lbfgs')

    plt.title('LogisticRegression, solver=lbfgs, regularization=L2')

    clf = clf.fit(train_data[0], train_data[1])

    predictions = clf.predict(test_data[0])
    # predictions = [x[0] for]

    if draw_roc_curve:
        draw_roc_curve_plotlib(test_data[1], predictions, limit, color)

    if print_graph:
        print_graph_graphviz(clf)

# plt.show()
plt.savefig("output/graphs/logreg-lbfgs-l2.svg")





