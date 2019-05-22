from src.chpdb import cursor
import datetime
import numpy as np
from src.parser import parse_value


# queries the database for preceding sensor readings
def get_sensor_data(date, machineID, sensors, count):
    query = "SELECT opkdato, {} " \
            "FROM opkald2 " \
            "WHERE anlaegId = {} " \
            "AND opkdato < '{}' " \
            "ORDER BY opkdato DESC " \
            "LIMIT {};".format(
                ','.join(sensors),
                machineID,
                date,
                count
            )

    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) < count:
        return False, False

    # first returned values are dates of messages
    dates = [val[0] for val in result]
    # rest of returned values are sensor readings
    sensors = [val[1:] for val in result]
    return dates, sensors


# iterates over the database values and puts the values in an array
def parse_sensors(sensor_rows, sensor_names, aggregate):
    values = []
    i = 0
    # iterate over all sensor names to be produced
    for sensor_name in sensor_names:
        # iterate over all opkald2 messages returned
        for row in sensor_rows:
            # parse the value according to the sensor name
            value = parse_value(sensor_name, row[i])

            if (None in value) or (value is None):
                raise Exception("Invalid value found in this sample. Column name {}!".format(sensor_name))

            # if aggregation is enabled, output all values
            # otherwise just output average
            if aggregate:
                values.append(value)
            else:
                value = sum(value) / len(value)
                values.append(value)
        i += 1
    return values


# compute time intervals between opkald dates and current reference datetime
def parse_dates(dates, reference):
    intervals = []
    for i in range(0, len(dates)):
        delta = reference - dates[i]
        intervals.append(delta.total_seconds())
    return intervals


def aggregate_values(parsed_sensors, sensor_readings_count):
    result = []

    for i in range(0, len(parsed_sensors)):
        # aggregated = []
        # for j in range(sensor_readings_count):
        #     aggregated.append(parsed_sensors[i + j])
        # result.append(np.mean(parsed_sensors[i]))  # arithmetic mean
        result.append(np.var(parsed_sensors[i]))  # variance

    return result


# function retrieves specified number of sensor readings prior to a specified time
def fetch_sensors(datetime, machine_id, sensor_names, sensor_readings_count, aggregate=False):
    res = []
    dates, sensor_readings = get_sensor_data(datetime, machine_id, sensor_names, sensor_readings_count)

    if not dates and sensor_readings:
        return []

    result_sensors = parse_sensors(sensor_readings, sensor_names, aggregate)
    if aggregate:
        result_sensors = aggregate_values(result_sensors, sensor_readings_count)

    res.extend(result_sensors)
    res.extend(parse_dates(dates, datetime))

    return res


# test
# fetch_sensors(datetime.datetime(2019, 12, 5), 1000711803, ['actual_rpm', 'storage_fill'], 5)
