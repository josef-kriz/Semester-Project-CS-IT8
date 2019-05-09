from src.classification_print_tools import print_data_statistics


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