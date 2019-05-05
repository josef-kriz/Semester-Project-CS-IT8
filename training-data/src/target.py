from .chpdb import cursor
import datetime


# Returns 0 if no misfire kills in the next 24hours, 1 otherwise.
def get_target(ref_datetime, machine_id):
    cursor.execute(f'SELECT MIN(opkdato) FROM opkald2 WHERE anlaegId = {machine_id};')
    date = cursor.fetchone()[0]

    if date is None:
        raise Exception(f'No message found for machine #{machine_id} in the opkald2 table!')

    end_date = date + datetime.timedelta(days=1)

    cursor.execute(f'SELECT COUNT(*) FROM anlaegshaendelser WHERE anlaeg_id = {machine_id} AND dato > "{ref_datetime}" AND dato < "{end_date}" AND misfire_shutdown = 1;')
    shutdown_count = cursor.fetchone()[0]

    if shutdown_count > 0:
        return 1
    else:
        return 0
