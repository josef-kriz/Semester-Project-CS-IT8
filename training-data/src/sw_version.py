from .chpdb import cursor


# Returns the median of all software versions of the given machine for the last x messages from the given date
def get_sw_version(ref_datetime, machine_id, x):
    # get the timestamp of the x'th last message that will server as the start of the interval
    cursor.execute(f'SELECT opkdato\
                        FROM opkald2\
                        WHERE anlaegId = {machine_id}\
                            AND opkdato <= "{ref_datetime}"\
                        ORDER BY opkdato DESC\
                        LIMIT {x};\
    ')
    first_message = cursor.fetchall()[x - 1][0]

    cursor.execute(f'SELECT softwareversion\
                        FROM anlaeg_config\
                        WHERE anlaeg_id = {machine_id}\
                            AND opkdato >= "{first_message}"\
                            AND opkdato <= "{ref_datetime}"\
                        ORDER BY opkdato DESC\
                        LIMIT {x};\
    ')
    versions = [x[0] for x in cursor.fetchall()]
    if len(versions) == 0:
        cursor.execute(f'SELECT softwareversion\
                        FROM anlaeg_config\
                        WHERE anlaeg_id = {machine_id}\
                        ORDER BY opkdato DESC\
                        LIMIT 1;\
    ')
        date = cursor.fetchone()[0]

        if date is None:
            raise Exception(f'No config found for machine #{machine_id} in the anlaeg_config table!')

        return [int(date)]

    return [int(max(set(versions), key=versions.count))]
