from .chpdb import cursor


# Returns list [misfires in the past, misfire kills in the past]
def get_past_misfires(ref_datetime, machine_id):
    cursor.execute(f'SELECT MIN(opkdato) FROM opkald2 WHERE anlaegId = {machine_id};')
    date = cursor.fetchone()[0]

    if date is None:
        raise Exception(f'No message found for machine #{machine_id} in the opkald2 table!')

    cursor.execute(f'SELECT COUNT(*) FROM anlaegshaendelser WHERE anlaeg_id = {machine_id} AND dato > "{date}" AND dato < "{ref_datetime}" AND haendelse = 112;')
    misfire_count = cursor.fetchone()[0]

    cursor.execute(f'SELECT COUNT(*) FROM anlaegshaendelser WHERE anlaeg_id = {machine_id} AND dato > "{date}" AND dato < "{ref_datetime}" AND misfire_shutdown = 1;')
    misfire_kill_count = cursor.fetchone()[0]

    return [misfire_count, misfire_kill_count]