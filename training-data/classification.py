from src.classification_print_tools import print_graph_graphviz, print_data_split_statistics, draw_roc_curve_plotlib
from src.classification_data_tools import split_data
from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn import tree
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn import svm
from sklearn import linear_model
import matplotlib.pyplot as plt
import pickle


def run_experiment(clf, title, file_name, ratio, limits, test_on_train=False, scale=False):
    for [limit, color] in limits:
        train_data, test_data = split_data(features, targets, ratio, limit)
        plt.title(title)

        if scale:
            clf = clf.fit(preprocessing.scale(train_data[0]), train_data[1])
        else:
            clf = clf.fit(train_data[0], train_data[1])

        if test_on_train:
            test_data = train_data

        if scale:
            predictions = clf.predict(preprocessing.scale(test_data[0]))
        else:
            predictions = clf.predict(test_data[0])

        if draw_roc_curve:
            draw_roc_curve_plotlib(test_data[1], predictions, limit, color)

        if print_graph:
            print_graph_graphviz(clf)

    plt.savefig(file_name)
    plt.clf()


# CONFIG
training_test_ratio = 0.7
shuffle_data = True
print_graph = False
draw_roc_curve = True
file_name = 'output/190523-full-5d-aggr-mean.pickle'
output_path_base = 'output/graphs/final-mean-5d/final-'
negative_sample_limits = [
    [800, 'blue'],
    [1000, 'darkorange'],
    [1500, 'green'],
    [2000, 'red'],
    [10000, 'brown']
]

with open(file_name, 'rb') as f:
    data = pickle.load(f)

features = data[0]
targets = data[1]

print_data_split_statistics(targets)

if shuffle_data:
    features, targets = shuffle(features, targets)

# pickle.dump([features, targets], open('output/final-variance-shuffled.pickle', 'wb'))

for limit in [None, 4, 8, 16, 32]:
    run_experiment(
        tree.DecisionTreeClassifier(max_depth=limit),
        "DecisionTreeClassifier, max_depth={}".format(limit),
        "{}tree-d{}.pdf".format(output_path_base, limit),
        training_test_ratio,
        negative_sample_limits,
    )

run_experiment(
    svm.SVC(cache_size=4000, class_weight='balanced'),
    "SVC, balanced weights",
    "{}svc-scaled-balanced.pdf".format(output_path_base),
    training_test_ratio,
    negative_sample_limits,
    False,
    True
)

run_experiment(
    svm.SVC(cache_size=4000),
    "SVC",
    "{}svc-scaled-not-balanced.pdf".format(output_path_base),
    training_test_ratio,
    negative_sample_limits,
    False,
    True
)

run_experiment(
    ensemble.RandomForestClassifier(),
    "RandomForestClassifier",
    "{}random-forest.pdf".format(output_path_base),
    training_test_ratio,
    negative_sample_limits
)

# run_experiment(
#     neighbors.KNeighborsClassifier(n_neighbors=4),
#     "KNeighborsClassifier",
#     "{}knn-4.pdf".format(output_path_base),
#     training_test_ratio,
#     negative_sample_limits
# )
#
# for [solver, penalty] in [['liblinear', 'l2'], ['lbfgs', 'none'], ['saga', 'elasticnet'], ['liblinear', 'l1']]:
#     run_experiment(
#         linear_model.LogisticRegression(solver=solver, penalty=penalty, l1_ratio=0.5),
#         "LogisticRegression, solver={}, regularization={}".format(solver, penalty.upper()),
#         "{}logreg-{}-{}.pdf".format(output_path_base, solver, penalty.upper()),
#         training_test_ratio,
#         negative_sample_limits
#     )