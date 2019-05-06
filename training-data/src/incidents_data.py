from src.chpdb import cursor
import datetime


def fill_in_empty_values(db_data, incident_ids):
    res = [0] * len(incident_ids)
    for row in db_data:
        incident_id = row[0]
        incident_count = row[1]
        index = incident_ids.index(incident_id)
        res[index] = incident_count
    return res


def get_incidents_counts(machine_id, interval_start, interval_end, incident_ids):
    query = "SELECT haendelse, COUNT(1) " \
            "FROM anlaegshaendelser " \
            "WHERE haendelse IN ({}) " \
            "AND anlaeg_id = {} " \
            "AND dato > '{}' " \
            "AND dato < '{}' " \
            "GROUP BY haendelse " \
            "ORDER BY haendelse;".format(
                ','.join(str(x) for x in incident_ids),
                machine_id,
                interval_start,
                interval_end
            )
    # print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    # print(len(result))
    return result


def fetch_incidents(datetime, machine_id, interval, incident_ids):
    interval_start = datetime - interval
    interval_end = datetime
    incident_counts = get_incidents_counts(machine_id, interval_start, interval_end, incident_ids)
    return fill_in_empty_values(incident_counts, incident_ids)


# res = fetch_incidents(
#     datetime.datetime(year=2017, month=12, day=1),
#     1000711803,
#     datetime.timedelta(days=120),
#     [78, 4, 112]
# )
# print(res)
