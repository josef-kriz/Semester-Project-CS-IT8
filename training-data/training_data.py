import datetime
import pickle
from src.chpdb import cursor
from src.incidents_data import fetch_incidents
from src.sensor_data import fetch_sensors
from src.life_span import get_life_span
from src.sw_version import get_sw_version
from src.past_misfires import get_past_misfires
from src.machine_type import get_machine_type
from src.target import get_target
from data.misfire_shutdown_machines import training_machine_ids
from random import shuffle
# import graphviz

settings = {
    'machines_count': 100,
    'incidents': [1, 5, 6, 7, 10, 19, 20, 21, 49, 61, 62, 63, 64, 65, 66, 68, 76,
                  79, 80, 81, 82, 83, 89, 100, 102, 103, 112, 113, 123, 130, 133],
    'incidents_past_interval': datetime.timedelta(days=7),
    'sensors': ['aktuel_elproduktion','ab','ac','actual_map_pressure','actual_powerstep_position','actual_rpm',
                'ak','anlaeggets_elproduktion','av','cv_psu_voltage','ecu_pcb_temp','ecu_vandtemp','flow_control_fremloebs',
                'flow_control_retur','flow_control_setpoint','lk','lw','mk','mv','stopminutter',
                'varmefordeler_printtemparatur'],
    'sensors_samples': 5,
    'misfire_interval': datetime.timedelta(days=1),
    'sampling_interval': datetime.timedelta(days=1),
    'training_output': 'output/training.pickle',
    'test_output': 'output/test.pickle'
}


def get_machines(count=1000):
    shuffle(training_machine_ids)
    if count > len(training_machine_ids):
        return training_machine_ids
    else:
        return training_machine_ids[:count]


def is_machine_valid(machine_id, start, end):
    query = "SELECT COUNT(1) " \
            "FROM anlaegshaendelser " \
            "WHERE anlaeg_id = {} " \
            "AND dato >= \"{}\" " \
            "AND dato <= \"{}\" " \
            "AND misfire_shutdown = 1;".format(machine_id, start, end)
    cursor.execute(query)
    return cursor.fetchone()[0] >= 1


def sample_machine(machine_id, ref_settings):
    start_date = get_machine_start_date(machine_id, ref_settings)

    if start_date == False:
        return False, False

    end_date = get_machine_end_date(machine_id)

    if not is_machine_valid(machine_id, start_date, end_date):
        print("\tSampling cancelled. No misfire shutdowns found in sampling period.")
        return False, False

    print("\tSampling from", start_date, "to", end_date)

    current_date = start_date

    samples_data = []
    samples_targets = []
    while current_date < end_date:
        try:
            step_data, step_target = sampling_step(machine_id, current_date, ref_settings)
            samples_data.append(step_data)
            samples_targets.append(step_target)
        except Exception as e:
            str(e)
            # print("Sample skipped.", str(e))

        current_date += ref_settings['sampling_interval']

    print("\tCreated", len(samples_targets), "samples.", len([x for x in samples_targets if x == 1]), "of them have misfire kills.")
    feature_lengths = [len(x) for x in samples_data]
    if len(feature_lengths) != 0:
        print("\tAverage features array length is", sum(feature_lengths) / len(feature_lengths))
    return samples_data, samples_targets


def get_machine_start_date(machine_id, settings):
    first_sensors_moment = get_start_sensors(machine_id, settings['sensors_samples'])
    first_incidents_moment = get_start_incidents(machine_id, settings['incidents_past_interval'])
    if first_sensors_moment is None or first_incidents_moment is None:
        return False
    else:
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
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return result[0]


def get_start_incidents(machine_id, time_interval):
    query = "SELECT dato " \
            "FROM anlaegshaendelser " \
            "WHERE anlaeg_id = {} " \
            "ORDER BY dato ASC " \
            "LIMIT 1;".format(machine_id)
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return None
    return result[0] + time_interval


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
    # print(step_data, step_target)
    return step_data, step_target


def sample_machines_set(machine_ids):
    features = []
    targets = []
    for index, id in enumerate(machine_ids):
        print("#" + str(id) + " - " + str(index + 1) + " of " + str(len(machine_ids)))
        machine_features, machine_targets = sample_machine(id, settings)
        if machine_features and machine_targets:
            features.extend(machine_features)
            targets.extend(machine_targets)
    return [features, targets]


training_file = open(settings['training_output'], "wb")
test_file = open(settings['test_output'], "wb")

machines = get_machines(settings['machines_count'])
split_index = int(len(machines) * 0.7)

training_machines = machines[:split_index]
test_machines = machines[split_index:]

print("Training machines:")
pickle.dump(sample_machines_set(training_machines), training_file)
print("Test machines:")
pickle.dump(sample_machines_set(test_machines), test_file)

cursor.close()
