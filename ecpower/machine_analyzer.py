import mysql.connector
import pandas as pd
import numpy as np
from dumper.src.parser import parse_value
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import os

# machine_id = 1005171049
# machine_id = 2000410280
machine_id = 1100405472
db_row_limit = 10000  # limit for the number of rows being queried from the database
interval = 'H'  # resampling time interval (handbook: http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects)
cluster_threshold = 2  # number of misfires in the interval for them to be considered as a cluster
output_path = f'out/{machine_id}_plots'  # the output path for plots

# define the MySQL connection
db = mysql.connector.connect(
    host="192.38.56.161",
    port="3306",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)
cursor = db.cursor()


# fetches all the misfire incidents for the given machine from the anlaeghaendelser table
def get_misfires(db_cursor, machine, row_limit=1000):
    # execute the query
    # get all the misfire incidents for the given machine
    db_cursor.execute(
        f'SELECT * FROM anlaegshaendelser WHERE anlaeg_id = {machine} AND haendelse = 112 LIMIT {row_limit};')

    # turn the result into a pandas DataFrame
    return pd.DataFrame(db_cursor.fetchall(),
                        columns=['id', 'dato', 'effekt', 'haendelse', 'opkald_id', 'anlaeg_id', 'opkdato', 'sortorder',
                                 'groupId', 'admin', 'timeZone'])


# resample the data to smaller chunks and sum them up
def resample_misfires(data, offset):
    # create a new column with the date in correct format
    data['date'] = pd.to_datetime(data['dato'])

    # create a new DataFrame using the new date column from result
    # put 1 for misfire count and default dot size of 50
    dates = data.loc[:, ['date']]
    dates['size'] = pd.Series(np.full((dates.shape[0],), 50, dtype=int))
    dates['misfires'] = pd.Series(np.ones((dates.shape[0],), dtype=int))

    # resample the dates dataframe according to the given interval
    return dates.resample(offset, on='date').sum()


# fetches all the calls for the given machine from the opkald2 table
def get_calls(db_cursor, machine, row_limit=10000):
    # execute the query
    # get all the calls for the given machine
    db_cursor.execute(f'SELECT * FROM opkald2 WHERE anlaegId = {machine} LIMIT {row_limit};')

    # turn the result into a pandas DataFrame
    return pd.DataFrame(db_cursor.fetchall(),
                        columns=['id', 'dateCreated', 'opkdato', 'anlaegId', 'kaldsgrund', 'driftsform', 'tankfoeler1',
                                 'tankfoeler2', 'tankfoeler3', 'kogealarm', 'olietryk', 'vandalarm', 'ekstraalarm',
                                 'driftsminutter', 'husets_elforbrug', 'anlaeggets_elproduktion', 'total_driftstid',
                                 'antal_starter', 'total_stilstandstid', 'varmepumpe1_indkoblet', 'varmepumpe1_starter',
                                 'varmepumpe2_indkoblet', 'varmepumpe2_starter', 'lavt_forbrug', 'underskud',
                                 'totalt_underskud', 'tab', 'gasalarm', 'fasefejl', 'rumtemp', 'antennesignal',
                                 'stopminutter', 'motorvaern', 'el_solgt', 'varmeproduktion', 'braendselsforbrug',
                                 'olieskift_ns', 'olieskift_nl', 'olieskift_nc', 'olieskift_nh', 'fly_start', 'fly_hot',
                                 'fly_trailing_hot', 'fly_cool', 'fly_coefficient', 'storage_fill', 'fd', 'af', 'um',
                                 'debug_info', 'brandalarm', 'odd_storage', 'varmefordeler_printtemparatur', 'mv', 'mk',
                                 'lw', 'lk', 'vr', 'varmefordeler_transport', 'lager_procent', 'sa', 'sb', 'ht', 'hb',
                                 'flow_control_setpoint', 'flow_control_fremloebs', 'flow_control_retur', 'av', 'st',
                                 'ps', 'fl', 'ev', 'fv', 'mp', 'hp', 'fm', 'fp', 'gw', 'gs', 'gt', 'cr',
                                 'gassikker_printtemp', 'flowcontrolusersetpoint', 'lr', 'datasampling', 'fejlkontrol',
                                 'fejlposition', 'aa', 'ab', 'ac', 'ad', 'ae', 'ag', 'ah', 'ai', 'aj', 'ak', 'am', 'an',
                                 'ao', 'uid', 'stempel', 'rs', 'cv_psu_voltage', 'last_rejected_start_reason',
                                 'wf_high_return_temp', 'ecu_pcb_temp', 'ecu_vandtemp', 'ecu_psu_voltage', 'misfire_1',
                                 'misfire_2', 'injector_current', 'ignitor_current', 'nb_current', 'start_map_pressure',
                                 'power_step_jitter', 'wot_map_pressure', 'wct_map_pressure', 'actual_map_pressure',
                                 'actual_powerstep_position', 'actual_ventil_position', 'actual_injector_time',
                                 'actual_rpm', 'requested_power', 'aim_power', 'lambda_setpoint', 'lambda_voltage',
                                 'map_offset', 'ignition_angel', 'dwell_time', 'aktuel_elproduktion', 'load_level',
                                 'loadsharer_totalconsumption', 'misfire_leds', 'misfire_log', 'lgvgp', 'bl_engineval',
                                 'bq_flowmastervalveposition', 'bm_flowmastersrctemp', 'bn_flowmasterbypasstemp',
                                 'bp_flowmasterpsuvoltage', 'bo_flowmasterpcbtemp', 'br_aktuelelproduktion',
                                 'bs_antalgeneratorstart', 'bx_nspfase1', 'by_nspfase2', 'bz_nspfase3',
                                 'ca_netfrekvens', 'reginaInstance', 'cjManualStatus', 'ckAuxTempTrackerSensor1',
                                 'clAuxTempTrackerSensor2', 'cmAuxTempTrackerSensor3', 'cnAuxTempTrackerSensor4',
                                 'CQVFMasterSourceTempActive', 'CSSWValidationResult', 'DINumberOfErrorCalls',
                                 'DKBoilerReleaseStatus', 'DOSurgeProtecterStatus', 'DUHPC1ReleaseTime',
                                 'GJHPC1ReleaseStatus', 'GEPMH1ReleaseTime', 'GFPMH1OperationalTime',
                                 'GOPMH2OperationalTime', 'GGPMH1HpvTemp', 'GPPMH2HpvTemp', 'GHPMH1HpkTemp',
                                 'GQPMH2HpkTemp', 'GIPMH1ReleaseStatus', 'GRPMH2ReleaseStatus']).set_index(
        'id').replace({pd.np.nan: None})


# draw and save the plots
def draw_clusters(data, offset, path):
    if not os.path.isdir(path):
        os.mkdir(path)

    register_matplotlib_converters()

    plt.scatter(data.index, data['misfires'], s=data['size'], c='red')
    plt.xticks(rotation='vertical')
    plt.xlabel('Time')
    plt.ylabel(f'# of occurrences in {offset}')
    plt.tight_layout()
    plt.savefig(f'{output_path}/clusters.png')
    # plt.show()
    plt.clf()


print(f'Analysis of machine #{machine_id}:')

misfires = get_misfires(cursor, machine_id, db_row_limit)

print(f'\t{len(misfires)} misfires found')

resampled = resample_misfires(misfires, interval)

# get all rows with misfire count greater than cluster_threshold
clusters = resampled.loc[resampled['misfires'] >= cluster_threshold]

print(f'\t{len(clusters)} clusters found where at least {cluster_threshold} happened in {interval}.')

calls = get_calls(cursor, machine_id, db_row_limit)

print(f'\t{len(calls)} calls found')

# parse all sensor values
for column in calls:
    calls[column] = calls[column].apply(lambda x: parse_value(column, x))

# print(calls.head())

draw_clusters(resampled, interval, output_path)
print(f'\tplots saved to {output_path}')
