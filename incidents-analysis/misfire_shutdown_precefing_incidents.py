from chpdb import cursor
import pickle
import sys
import datetime


# iterates over all clusters of a group, queries the database and accumulates the statistics
def get_group_stats(cursor, stats, intervals, group):
    group_stats = {}
    for index, row in enumerate(group):
        # print status message every time 30 clusters are finished
        if (index+1) % 30 == 0:
            print("\t" + str(index+1) + " of " + str(len(group)))
        # store database response in a map
        group_stats[index] = (get_cluster_stats(cursor, row, intervals))
    print("Parsing group data...")
    for incident_data in group_stats.values():
        # accumulate responses for every cluster into group statistics
        stats = parse_group_stats(stats, incident_data, intervals)
    return stats


# queries the database for preceding incidents
def get_cluster_stats(cursor, row, intervals):
    data = {}
    for interval in intervals:
        start = row[0] - datetime.timedelta(seconds=interval)
        query = "SELECT haendelse, COUNT(*) FROM anlaegshaendelser " \
                " WHERE anlaeg_id = " + str(row[1]) + " AND dato < \"" + str(row[0]) + "\" AND " \
                " dato > \"" + str(start) + "\" GROUP BY haendelse ORDER BY haendelse;"
        cursor.execute(query)
        data[interval] = cursor.fetchall()
    return data


# accumulate group statistics into a map where the key is error code
# we keep information about the count of incident clusters that had certain preceding incident
# we also keep the number of such preceding incidents that occured in the whole group
def parse_group_stats(stats, data, intervals):
    for interval in intervals:
        for row in data[interval]:
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
                stats[code][interval]['clusters'] += 1
                stats[code][interval]['total_count'] += count
            except KeyError:
                # create it if it does not exist yet
                stats[code][interval] = {
                    'clusters': 1,
                    'total_count': count
                }
    return stats


# goes through the dictionary of statistics and prints the relative counts of clusters that experienced certain
# incident in the interval prior to the cluster
def print_stats(stats, data_intervals, output, count):
    groups = sorted(data_intervals)

    # write a header with group labels
    output.write('Error code')
    for group in groups:
        output.write(',' + str(group))
    output.write('\r\n')

    # write statistics for each preceding error code in a line
    sorted_codes = sorted(stats.keys())
    for error_code in sorted_codes:
        output.write(str(error_code))
        for group in groups:
            try:
                value = stats[error_code][group]['clusters']
            except KeyError:
                value = 0
            output.write("," + str((value / count)))
        output.write('\r\n')

    output.close()


data_intervals = [1209600,604800,86400,3600]
# output = sys.argv[4]
output = 'data/test.csv'

dest_file = open(output, 'w')

# go through all cluster groups and collect the data into a dictionary
cursor.execute('SELECT opkdato, anlaeg_id FROM anlaegshaendelser WHERE haendelse = 112 AND misfire_shutdown = 1 ORDER BY opkdato')
misfires = cursor.fetchall()
stats = {}
stats = get_group_stats(cursor, stats, data_intervals, misfires)


# print the data into a csv file
print_stats(stats, data_intervals, dest_file, len(misfires))