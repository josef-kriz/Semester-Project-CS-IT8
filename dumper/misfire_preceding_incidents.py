from chpdb import cursor
import pickle
import sys
import datetime


def get_group_stats(cursor, groupIndex, group, stats):
    group_stats = {}
    for index, cluster in enumerate(group):
        if (index+1) % 30 == 0:
            print("\t" + str(index+1) + " of " + str(len(group)))
        group_stats[index] = (get_cluster_stats(cursor, cluster))
    print("Parsing group data...")
    for index, row in group_stats.items():
        stats = parse_group_stats(stats, groupIndex, row)
    return stats


def get_cluster_stats(cursor, cluster):
    start = cluster.date - datetime.timedelta(seconds=interval)
    query = "SELECT haendelse, COUNT(*) FROM anlaegshaendelser " \
            " WHERE anlaeg_id = " + str(cluster.machineID) + " AND dato < \"" + str(cluster.date) + "\" AND " \
            " dato > \"" + str(start) + "\" GROUP BY haendelse ORDER BY haendelse;"
    cursor.execute(query)
    return cursor.fetchall()


def parse_group_stats(stats, group, res):
    for row in res:
        code = row[0]
        count = row[1]
        try:
            stats[code][group] = count
        except KeyError:
            stats[code] = {}
            stats[code][group] = count
    return stats


def print_stats(groups, stats, data_interval, path):
    f = open(path, 'w')
    f.write('Error code,')
    for group_index in range(0, len(groups)):
        lower_bound = group_index * data_interval / 60
        upper_bound = (1 + group_index) * data_interval / 60
        if group_index == 0:
            f.write("Single misfires,")
        else:
            f.write("Grp #" + str(group_index - 1) + ': ' + str(int(lower_bound)) + '-' + str(int(upper_bound)) + 'min,')
    f.write('\r\n')

    f.write('Number of clusters,')
    for group_index in range(0, len(groups)):
        no = len(groups[group_index])
        f.write(str(no) + ',')
    f.write('\r\n')

    sorted_codes = sorted(stats.keys())
    for error_code in sorted_codes:
        f.write(str(error_code))
        for group_index in range(0, len(groups)):
            try:
                value = stats[error_code][group_index]
            except KeyError:
                value = 0
            f.write("," + str(value))
        f.write('\r\n')

    f.close()


path = sys.argv[1]
# path = 'data/clustersgrouped.rick'
data_interval = int(sys.argv[2])
# data_interval = 900
interval = int(sys.argv[3])
# interval = 1209600
output = sys.argv[4]
# output = 'data/preceding-events-stats.csv'

source_file = open(path, 'rb')
grouped_clusters = pickle.load(source_file)

stats = {}
for index, group_index in enumerate(grouped_clusters):
    print(str(index+1) + " of " + str(len(grouped_clusters)) + " - # of clusters: " + str(len(group_index)))
    stats = get_group_stats(cursor, index, group_index, stats)

print_stats(grouped_clusters, stats, data_interval, output)