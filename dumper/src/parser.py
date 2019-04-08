def parse_value(name, value):
    if value is None or value == '' or value == ' ':
        return None
    try:
        # print(name)
        for parser in parsers:
            if name in parser[3]:
                return parser[0](parser[1], parser[2], value)
        return int(value)
    except:
        print('Parsing of', name, 'failed on value', value)


def keep_as_is(l, p, value):
    del l, p
    return value


def datetime_parser(l, p, value):
    del l, p
    return value


def temp_parser(length, precision, value):
    # print(length, precision, value)
    return multiple_values_parser(length, value, (lambda val: temp_parser_inner(val, precision)))


def temp_parser_inner(value, precision):
    if value == 'ABSENT':
        return None
    if value == 'ERRORS':
        return None
    return signed_parser_inner(value, precision)


def unsigned_parser(length, precision, value):
    return multiple_values_parser(length, value, (lambda val: unsigned_parser_inner(val, precision)))


def unsigned_parser_inner(value, precision):
    return float(value) / pow(10, precision)


def signed_parser(length, precision, value):
    return multiple_values_parser(length, value, (lambda val: signed_parser_inner(val, precision)))


def signed_parser_inner(value, precision):
    sign = value[0]
    val = value[1:]
    val = unsigned_parser_inner(val, precision)
    if sign == '0':
        return -1 * val
    return val


def multiple_values_parser(length, value, parser):
    if len(value) > length:
        return list(map(parser, split_length(value, length)))
    return parser(value)


def split_length(seq, length):
    parts = []
    i = 0
    while True:
        if i + length > len(seq):
            break
        parts.append(seq[i:i + length])
        i = i + length
    return parts


parsers = [
    [unsigned_parser, 3, 2, ['aa', 'load_level', 'bl_engineval', 'bq_flowmastervalveposition', 'fp', 'hp']],
    [unsigned_parser, 5, 2, ['ab', 'actual_injector_time', 'aktuel_elproduktion', 'br_aktuelelproduktio']],
    [unsigned_parser, 3, 1,
     ['bp_flowmasterpsuvoltage', 'cv_psu_voltage', 'dwell_time', 'ecu_psu_voltage', 'ignition_angel', 'ignitor_current',
      'injector_current', 'varmefordeler_transport']],
    [unsigned_parser, 3, 2, ['nb_current']],
    [unsigned_parser, 4, 2, ['ca_netfrekvens', 'fl', 'fm']],
    [temp_parser, 6, 2,
     ['varmefordeler_printtemparatur', 'st', 'mv', 'gassikker_printtemp', 'ad', 'ae', 'ag', 'ah', 'an', 'ao',
      'bm_flowmastersrctemp', 'bn_flowmasterbypasstemp', 'bo_flowmasterpcbtemp', 'ckAuxTempTrackerSensor1',
      'clAuxTempTrackerSensor2', 'cmAuxTempTrackerSensor3', 'cnAuxTempTrackerSensor4', 'DXHPC1HPVTemp', 'DYHPC1HPKTemp',
      'ecu_vandtemp', 'EGHPC2HPVTemp', 'EIHPC2HPKTemp', 'EQHPC3HPVTemp', 'ERHPC3HPKTemp', 'ecu_pcb_temp',
      'FAHPC4HPVTemp', 'FCHPC4HPKTemp', 'flow_control_fremloebs', 'FKHPC5HPVTemp', 'FNHPC5HPKTemp',
      'flow_control_setpoint', 'flow_control_retur', 'flowcontrolusersetpoint', 'FYHPC6HPVTemp', 'FZHPC6HPKTemp',
      'GGPMH1HpvTemp', 'GHPMH1HpkTemp', 'GPPMH2HpvTemp', 'GQPMH2HpkTemp', 'gt', 'hb', 'HDPMH3HpvTemp', 'HFPMH3HpkTemp',
      'HNPMH4HpvTemp', 'HOPMH4HpkTemp', 'ht', 'HYPMH5HpvTemp', 'HZPMH5HpkTemp', 'IKPMH6HpvTemp', 'ILPMH6HpkTemp',
      'ISSmartStartBoardTemp', 'IXPMHStorageTemp', 'lk', 'lw', 'mk', 'ps', 'vr']],
    [signed_parser, 6, 0, ['ai', 'aj', 'ak', 'am']],
    [unsigned_parser, 5, 0, ['aim_power', 'av', 'misfire_1', 'lgvgp', 'requested_power']],
    [unsigned_parser, 4, 0,
     ['actual_map_pressure', 'start_map_pressure', 'map_offset', 'lambda_setpoint', 'lambda_voltage']],
    [unsigned_parser, 3, 0, ['bx_nspfase1', 'by_nspfase2', 'bz_nspfase3']],
    [datetime_parser, 0, 0, ['dateCreated', 'opkdato', 'datasampling']],
    [keep_as_is, 0, 0, ['reginaInstance', 'misfire_log', 'cr']]  # what TODO with these columns?
]
