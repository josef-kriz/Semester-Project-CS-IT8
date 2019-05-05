import datetime
from src.chpdb import cursor
from src.incidents_data import fetch_incidents
from src.sensor_data import fetch_sensors
from src.life_span import get_life_span
from src.sw_version import get_sw_version
from src.past_misfires import get_past_misfires
from src.machine_type import get_machine_type
from src.target import get_target

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


def sample_machine(machine_id, ref_settings):
    start_date = get_machine_start_date(machine_id, ref_settings)
    end_date = get_machine_end_date(machine_id)
    current_date = start_date
    # print(start_date)
    # print(end_date)
    # print(current_date)
    samples_data = []
    samples_targets = []
    while current_date < end_date:
        step_data, step_target = sampling_step(machine_id, current_date, ref_settings)
        samples_data.append(step_data)
        samples_targets.append(step_target)
        current_date += ref_settings['sampling_interval']
    return samples_data, samples_targets


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


def sampling_step(machine_id, ref_datetime, ref_settings):
    step_data = []
    step_data.extend(
        # incidents
        fetch_incidents(
            ref_datetime,
            machine_id,
            ref_settings['incidents_past_interval'],
            ref_settings['incidents']
        ))
    # sensors
    step_data.extend(fetch_sensors(
        ref_datetime,
        machine_id,
        ref_settings['sensors'],
        ref_settings['sensors_samples']
    ))
    # life span
    step_data.extend(get_life_span(ref_datetime, machine_id))
    # software version
    step_data.extend(get_sw_version(ref_datetime, machine_id, ref_settings['sensors_samples']))
    # misfire kills & misfires
    step_data.extend(get_past_misfires(ref_datetime, machine_id))
    # type of machine
    step_data.extend(get_machine_type(machine_id))

    step_target = get_target(ref_datetime, machine_id)
    print(step_data, step_target)
    return step_data, step_target


machines = get_machines(1)
data = []
targets = []
for machine in machines:
    machine_samples, machine_targets = sample_machine(machine, settings)
    data.extend(machine_samples)
    targets.extend(machine_targets)

print(len(data), len(targets))

cursor.close()
