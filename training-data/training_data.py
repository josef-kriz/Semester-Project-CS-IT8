import datetime
from src.chpdb import cursor
from src.incidents_data import fetch_incidents
from src.sensor_data import fetch_sensors

settings = {
    'incidents': [78, 4, 112],
    'incidents_past_interval': datetime.timedelta(days=7),
    'sensors': ['actual_rpm', 'storage_fill'],
    'sensors_samples': 5,
    'misfire_interval': datetime.timedelta(days=1),
    'sampling_interval': datetime.timedelta(days=1)
}


def get_machines(count):
    cursor.execute("SELECT id "
                   "FROM anlaeg "
                   "ORDER BY RAND() "
                   "LIMIT {};".format(count))
    return [x[0] for x in cursor.fetchall()]


def sample_machine(machine_id, settings):
    start_date = get_machine_start_date(machine_id, settings)
    end_date = get_machine_end_date(machine_id)
    current_date = start_date
    # print(start_date)
    # print(end_date)
    # print(current_date)
    samples = []
    while current_date < end_date:
        samples.append(sampling_step(machine_id, current_date, settings))
        current_date += settings['sampling_interval']
    return samples


def sampling_step(machine_id, datetime, settings):
    data = []
    data.extend(
        fetch_incidents(
            datetime,
            machine_id,
            settings['incidents_past_interval'],
            settings['incidents']
        )
    )
    data.extend(
        fetch_sensors(
            datetime,
            machine_id,
            settings['sensors'],
            settings['sensors_samples']
        )
    )
    print(data)
    return data


def get_machine_start_date(machine_id, settings):
    first_sensors_moment = get_start_sensors(machine_id, settings['sensors_samples'])
    first_incidents_moment = get_start_incidents(machine_id, settings['incidents_past_interval'])
    return max(first_incidents_moment, first_sensors_moment)

def get_machine_end_date(machine_id):
    query = "SELECT opkdato " \
            "FROM opkald2 " \
            "WHERE anlaegId = {} " \
            "ORDER BY opkdato DESC " \
            "LIMIT 1;".format(machine_id)
    cursor.execute(query)
    return cursor.fetchone()[0]


def get_start_sensors(machine_id, sensor_samples_count):
    query = "SELECT opkdato " \
                    "FROM opkald2 " \
                    "WHERE anlaegId = {} " \
                    "ORDER BY opkdato " \
                    "LIMIT {}, 1;".format(
                        machine_id,
                        sensor_samples_count - 1
                    )
    cursor.execute(query)
    return cursor.fetchone()[0]


def get_start_incidents(machine_id, time_interval):
    query = "SELECT dato " \
            "FROM anlaegshaendelser " \
            "WHERE anlaeg_id = {} " \
            "ORDER BY dato ASC " \
            "LIMIT 1;".format(machine_id)
    cursor.execute(query)
    return cursor.fetchone()[0] + time_interval

machines = get_machines(1)
data = []
for machine_id in machines:
    data.append(sample_machine(machine_id, settings))

print(len(data))



