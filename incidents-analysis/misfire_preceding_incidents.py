from chpdb import cursor
import pickle
import sys
import datetime


# iterates over all clusters of a group, queries the database and accumulates the statistics
def get_group_stats(cursor, groupIndex, group, stats, interval):
    group_stats = {}
    for index, cluster in enumerate(group):
        # print status message every time 30 clusters are finished
        if (index+1) % 30 == 0:
            print("\t" + str(index+1) + " of " + str(len(group)))
        # store database response in a map
        group_stats[index] = (get_cluster_stats(cursor, cluster, interval))
    print("Parsing group data...")
    for index, row in group_stats.items():
        # accumulate responses for every cluster into group statistics
        stats = parse_group_stats(stats, groupIndex, row)
    return stats


# queries the database for preceding incidents
def get_cluster_stats(cursor, cluster, interval):
    start = cluster.date - datetime.timedelta(seconds=interval)
    query = "SELECT haendelse, COUNT(*) FROM anlaegshaendelser " \
            " WHERE anlaeg_id = " + str(cluster.machineID) + " AND dato < \"" + str(cluster.date) + "\" AND " \
            " dato > \"" + str(start) + "\" GROUP BY haendelse ORDER BY haendelse;"
    cursor.execute(query)
    return cursor.fetchall()


# accumulate group statistics into a map where the key is error code
# we keep information about the count of incident clusters that had certain preceding incident
# we also keep the number of such preceding incidents that occured in the whole group
def parse_group_stats(stats, group, res):
    for row in res:
        code = row[0]
        count = row[1]
        # just check whether error code dictionary exists
        try:
            boo = stats[code]
        except KeyError:
            # if there is an error incialize dictionary
            stats[code] = {}

        # check whether group dictionary was created
        try:
            stats[code][group]['clusters'] += 1
            stats[code][group]['total_count'] += count
        except KeyError:
            # create it if it does not exist yet
            stats[code][group] = {
                'clusters': 1,
                'total_count': count
            }
    return stats


# goes through the dictionary of statistics and prints the relative counts of clusters that experienced certain
# incident in the interval prior to the cluster
def print_stats(groups, stats, data_interval, output):
    groups = sorted(groups.items(), key=lambda x:x[0])
    # write number of clusters in each group
    output.write('Number of clusters,')
    for index, group in groups:
        no = len(group)
        output.write(str(no) + ',')
    output.write('\r\n')

    # write a header with group labels
    output.write('Error code,')
    for group_index, group in groups:
        lower_bound = (group_index - 1) * data_interval
        upper_bound = group_index * data_interval
        if group_index == 0:
            output.write("Single misfires,")
        else:
            output.write("Grp #" + str(group_index) + ': ' + str(int(lower_bound)) + '-' + str(int(upper_bound)) + 's,')
    output.write('\r\n')

    # write statistics for each preceding error code in a line
    sorted_codes = sorted(stats.keys())
    for error_code in sorted_codes:
        output.write(str(error_code))
        for group_index, group in groups:
            try:
                value = stats[error_code][group_index]['clusters']
            except KeyError:
                value = 0
            output.write("," + str((value / len(group))))
        output.write('\r\n')

    output.close()


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
dest_file = open(output, 'w')

# go through all cluster groups and collect the data into a dictionary
stats = {}
for index, group_index in grouped_clusters.items():
    # if index < 5:
    #     continue
    print(str(index+1) + " of " + str(len(grouped_clusters)) + " - # of clusters: " + str(len(group_index)))
    stats = get_group_stats(cursor, index, group_index, stats, interval)

# print the data into a csv file
print_stats(grouped_clusters, stats, data_interval, dest_file)