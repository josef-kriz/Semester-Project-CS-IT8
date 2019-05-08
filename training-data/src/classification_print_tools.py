from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn import tree
import matplotlib.pyplot as plt
import graphviz


# produce feature & target variable names
# this highly depends on the currently used dataset
def get_feature_target_names():
    feature_names = []
    feature_names.extend([f'Incident #{s}' for s in [1, 5, 6, 7, 10, 19, 20, 21, 49, 61, 62, 63, 64, 65, 66, 68, 76,
                                                     79, 80, 81, 82, 83, 89, 100, 102, 103, 112, 113, 123, 130, 133]])
    feature_names.extend([f'Reading #{n} for sensor {s}' for s in
                          ['aktuel_elproduktion', 'ab', 'ac', 'actual_map_pressure', 'actual_powerstep_position',
                           'actual_rpm',
                           'ak', 'anlaeggets_elproduktion', 'av', 'cv_psu_voltage', 'ecu_pcb_temp', 'ecu_vandtemp',
                           'lk', 'lw', 'mk', 'mv', 'stopminutter',
                           'varmefordeler_printtemparatur'] for n in range(1, 6)])
    feature_names.extend([f'Reading #{n} offset' for n in range(1, 6)])
    feature_names.extend(['Life span', 'SW version', 'Past misfire kills', 'Past misfires'])
    feature_names.extend([f'Machine type #{s}' for s in range(1, 9)])
    target_names = ['Misfire NO', 'Misfire YES']  # TODO this way or vice versa?
    return feature_names, target_names


# print decision tree classifier using graphviz
def print_graph_graphviz(clf):
    feature_names, target_names = get_feature_target_names()
    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=feature_names,
                                    class_names=target_names,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("iris")


def draw_roc_curve_plotlib(test_targets, predictions, limit, color):
    # compute roc curve and roc curve score
    auc = roc_auc_score(test_targets, predictions)
    fpr, tpr, thresholds = roc_curve(test_targets, predictions)

    print("Prediction statistics with limit of", limit)
    (precision, recall, _, _) = precision_recall_fscore_support(test_targets, predictions, average='macro')
    print("\tPrecision:", precision)
    print("\tRecall:", recall)

    # plot no skill line
    plt.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--')
    # plot the roc curve for the model
    plt.plot(fpr, tpr, color=color, lw=2, marker='.',
             label='limit {} - precision {:.3f}, recall {:.3f}'.format(limit, precision, recall))
    # add markers
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')


# print statistics about training and test data set
def print_data_statistics(train, test):
    print("Training set stats:")
    print_data_split_statistics(train[1])
    print("Test set stats:")
    print_data_split_statistics(test[1])


# print statistics about data set
def print_data_split_statistics(targets):
    misfire_count = len([x for x in targets if x == 1])
    print("\tSamples:", len(targets))
    print("\tSamples w shutdown:", misfire_count)
    print("\tSamples w\\ shutdown:", len(targets) - misfire_count)
