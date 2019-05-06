import datetime
from src.chpdb import cursor
from src.incidents_data import fetch_incidents
from src.sensor_data import fetch_sensors
from src.life_span import get_life_span
from src.sw_version import get_sw_version
from src.past_misfires import get_past_misfires
from src.machine_type import get_machine_type
from src.target import get_target
from sklearn import tree
# import graphviz

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
                   "ORDER BY RAND();")
    return [x[0] for x in cursor.fetchall()]


def sample_machine(machine_id, ref_settings):
    start_date = get_machine_start_date(machine_id, ref_settings)

    if start_date == False:
        return False, False

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
        if len(samples_data) > 20:
            break
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
    print(step_data, step_target)
    return step_data, step_target


fetch_machines = get_machines(3)
machines = fetch_machines[:2]
test_machines = fetch_machines[2:4]

# machines = [2100780010]
# test_machines = [2100780010]

data = []
targets = []
test_data = []
test_targets = []

for machine in machines:
    machine_samples, machine_targets = sample_machine(machine, settings)

    if machine_samples and machine_targets:
        data.extend(machine_samples)
        targets.extend(machine_targets)

for machine in test_machines:
    test_samples, test_targets = sample_machine(machine, settings)

    if test_samples and test_targets:
        test_data.extend(test_samples)
        test_targets.extend(test_targets)

print(len(data), len(targets))

clf = tree.DecisionTreeClassifier()
clf = clf.fit(data, targets)

test_sample1 = [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 23102330.0, 22552315.0, 22552315.0, 21552215.0, 21552215.0, 4003.0, 47290.0, 90567.0, 133847.0, 177125.0, 56684, '0010140002', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
test_sample2 = [7, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 22252245.0, 22102230.0, 22102230.0, 22252245.0, 22252245.0, 24880.0, 72306.0, 101180.0, 135341.0, 165746.0, 56684, '0010120003', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
test_sample3 = [0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 23102330.0, 23102330.0, 21252145.0, 21252145.0, 21252145.0, 34777.0, 63659.0, 117798.0, 148916.0, 180110.0, 56684, '0010120003', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

predictions = clf.predict(test_data)

correct_predictions = 0

for i in range(0, len(predictions)):
    if predictions[i] == test_targets[i]:
        correct_predictions += 1

print((correct_predictions / len(predictions)) * 100 + "%")

# dot_data = tree.export_graphviz(clf, out_file=None,
#                      # feature_names=iris.feature_names,
#                      # class_names=iris.target_names,
#                      filled=True, rounded=True,
#                      special_characters=True)
# graph = graphviz.Source(dot_data)
# graph.render("iris")

cursor.close()
