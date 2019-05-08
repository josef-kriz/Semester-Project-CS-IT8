from sklearn.utils import shuffle
from sklearn import tree
from sklearn import ensemble
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
import numpy as np
import pickle
import matplotlib.pyplot as plt
#import graphviz

#CONFIG
training_test_split = 0.7
shuffle_data = True
print_graph = False
draw_roc_curve = True

clf = tree.DecisionTreeClassifier()
#clf = ensemble.RandomForestClassifier()

def PrintGraph(clf):
    dot_data = tree.export_graphviz(clf, out_file=None,
                         # feature_names=iris.feature_names,
                         # class_names=iris.target_names,
                         filled=True, rounded=True,
                         special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("iris")

def DrawRocCurve(test_targets, predictions):
    np_test_targets = np.asarray(int_test_targets, dtype=np.int32)
    np_predictions = np.asarray(int_predictions, dtype=np.int32)

    # Compute micro-average ROC curve and ROC area
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    fpr["micro"], tpr["micro"], _ = roc_curve(np_test_targets.ravel(), np_predictions.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure()
    lw = 2
    plt.plot(fpr['micro'], tpr['micro'], color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc['micro'])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

with open('training.pickle', 'rb') as f:
    data = pickle.load(f)

    if shuffle_data:
        features, targets = shuffle(data[0], data[1])

    training_features = features[:int(len(data[0])*training_test_split)-1]
    training_targets = targets[:int(len(data[1])*training_test_split)-1]
    test_features = features[int(len(data[0])*training_test_split):]
    test_targets = targets[int(len(data[1])*training_test_split):]

    #counts the amount of samples with misfire kills in data
    counter = 0

    for i in range(len(data[1])):
        if data[1][i] == 1:
            counter += 1

    print(counter)
    print(len(data[1]))
    print('{0:.{1}f}'.format((counter / len(data[1]) * 100), 2) + '%')

clf = clf.fit(training_features, training_targets)

predictions = clf.predict(test_features)
int_test_targets = [int(i) for i in test_targets]
int_predictions = [int(i) for i in predictions]
print(precision_recall_fscore_support(int_test_targets, int_predictions, average='macro'))

if draw_roc_curve:
    DrawRocCurve(int_test_targets, int_predictions)

if print_graph:
    PrintGraph(clf)

