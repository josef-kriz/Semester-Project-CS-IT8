import mysql.connector
import json
import pickle
from model.entry import Entry
from src.parser import parse_value
from datetime import timedelta


def save_dump(data, path):
    f = open(path, "wb")
    pickle.dump(data, f)
    f.close()

# misfire_log
# reginaInstance
# gs
# opkdato, dateCreated, datasampling
columns = ['ekstraalarm','driftsminutter','driftsform','aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','am','an','ao','actual_powerstep_position','actual_injector_time','actual_rpm','antennesignal','aim_power','av','brandalarm','loadsharer_totalconsumption','load_level','aktuel_elproduktion','braendselsforbrug','misfire_leds','bl_engineval','bm_flowmastersrctemp','bn_flowmasterbypasstemp','bo_flowmasterpcbtemp','bp_flowmasterpsuvoltage','bq_flowmastervalveposition','br_aktuelelproduktion','bs_antalgeneratorstart','bx_nspfase1','by_nspfase2','bz_nspfase3','ca_netfrekvens','cjManualStatus','ckAuxTempTrackerSensor1','clAuxTempTrackerSensor2','cmAuxTempTrackerSensor3','cnAuxTempTrackerSensor4','actual_ventil_position','CQVFMasterSourceTempActive','CSSWValidationResult','cv_psu_voltage','debug_info','DINumberOfErrorCalls','DKBoilerReleaseStatus','DOSurgeProtecterStatus','DUHPC1ReleaseTime','DVHPC1OperationalTime','dwell_time','DXHPC1HPVTemp','DYHPC1HPKTemp','ecu_vandtemp','ecu_psu_voltage','EEHPC2ReleaseTime','EFHPC2OperationalTime','EGHPC2HPVTemp','EIHPC2HPKTemp','EOHPC3ReleaseTime','EPHPC3OperationalTime','EQHPC3HPVTemp','ERHPC3HPKTemp','el_solgt','ecu_pcb_temp','ev','EYHPC4ReleaseTime','EZHPC4OperationalTime','FAHPC4HPVTemp','husets_elforbrug','fp','FCHPC4HPKTemp','fd','flow_control_fremloebs','FIHPC5ReleaseTime','FJHPC5OperationalTime','FKHPC5HPVTemp','fl','fm','FNHPC5HPKTemp','flow_control_setpoint','flow_control_retur','flowcontrolusersetpoint','fv','FWHPC6ReleaseTime','FXHPC6OperationalTime','FYHPC6HPVTemp','FZHPC6HPKTemp','gasalarm','GEPMH1ReleaseTime','GFPMH1OperationalTime','GGPMH1HpvTemp','GHPMH1HpkTemp','GIPMH1ReleaseStatus','GJHPC1ReleaseStatus','GNPMH2ReleaseTime','GOPMH2OperationalTime','GPPMH2HpvTemp','GQPMH2HpkTemp','GRPMH2ReleaseStatus','gt','GUHPC2ReleaseStatus','gw','GZPMH3ReleaseTime','HAPMH3OperationalTime','hb','HDPMH3HpvTemp','HFPMH3HpkTemp','HGPMH3ReleaseStatus','HHHPC3ReleaseStatus','HLPMH4ReleaseTime','HMPMH4OperationalTime','HNPMH4HpvTemp','HOPMH4HpkTemp','hp','HQPMH4ReleaseStatus','HRHPC4ReleaseStatus','ht','HWPMH5ReleaseTime','HXPMH5OperationalTime','HYPMH5HpvTemp','HZPMH5HpkTemp','ignition_angel','IBPMH5ReleaseStatus','ICHPC5ReleaseStatus','anlaegId','ignitor_current','IIPMH6ReleaseTime','IJPMH6OperationalTime','IKPMH6HpvTemp','ILPMH6HpkTemp','IMPMH6ReleaseStatus','injector_current','IOHPC6ReleaseStatus','ISSmartStartBoardTemp','ITSmartStarterLastError','IXPMHStorageTemp','JBHRTMNoOfActivations','JCHRTMActivationTime','JDHRTMAverageLostPower','JIHrtmActive','kaldsgrund','kogealarm','lavt_forbrug','lk','lager_procent','lr','lw','actual_map_pressure','misfire_1','start_map_pressure','mk','map_offset','mp','mv','misfire_2','lambda_setpoint','lambda_voltage','nb_current','lgvgp','last_rejected_start_reason','olietryk','anlaeggets_elproduktion','ps','requested_power','rs','sa','sb','st','power_step_jitter','stopminutter','antal_starter','tab','total_driftstid','tankfoeler1','tankfoeler2','tankfoeler3','totalt_underskud','um','underskud','varmefordeler_transport','varmepumpe1_indkoblet','varmeproduktion','vr','varmepumpe1_starter','wf_high_return_temp','wct_map_pressure','varmepumpe2_indkoblet','wot_map_pressure','varmepumpe2_starter','olieskift_ns','id','vandalarm','total_stilstandstid','fasefejl','rumtemp','motorvaern','olieskift_nl','olieskift_nc','olieskift_nh','fly_start','fly_hot','fly_trailing_hot','fly_cool','fly_coefficient','storage_fill','odd_storage','varmefordeler_printtemparatur','gassikker_printtemp','fejlkontrol','fejlposition','uid','stempel']
# columns = ['anlaegId']

machineID = 1000005063

mydb = mysql.connector.connect(
    host="192.38.56.161",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)

my_cursor = mydb.cursor()

my_cursor.execute('SELECT opkdato, ' + ','.join(columns) + ' FROM opkald2 '
                  'WHERE anlaegId = ' + str(machineID) + ' AND '
                  'opkdato > "2015-08-07 10:33:29" '
                  'ORDER BY opkdato ASC')

print(my_cursor.statement)

result = my_cursor.fetchall()

array = []
for res in result:
    date = res[0]
    values = dict()
    i = 1
    for column in columns:
        values[column] = parse_value(column, res[i])
        i = i + 1
    array.append(Entry(date, values))

# acc = 0
# for i in range(0, len(array)):
#     if i + 1 >= len(array):
#         break
#     diff = array[i+1].date - array[i].date
#     # print("Message", array[i].values['id'], "received on", array[i].date, "seconds to next opkald2 entry:", diff.seconds)
#     acc = acc + diff.seconds

# print("Average number of seconds inbetween messages:", acc / len(array))

my_cursor.execute('SELECT dato, haendelse, effekt FROM anlaegshaendelser WHERE anlaeg_id = ' + str(machineID) + ' ORDER BY dato ASC')

result = my_cursor.fetchall()

for res in result:
    date = res[0]
    values = dict()
    values['error_code'] = res[1]
    values['effect'] = res[2]
    array.append(Entry(date, values, True))
    # print(values)

save_dump(array, 'data/' + str(machineID))

#kasper hello?

