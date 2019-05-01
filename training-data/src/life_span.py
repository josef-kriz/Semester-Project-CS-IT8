from .chpdb import cursor


# Find the oldest message for a given machine and return the time delta in seconds
def get_life_span(ref_datetime, machine_id):
    cursor.execute(f'SELECT MIN(opkdato) FROM opkald2 WHERE anlaegId = {machine_id};')
    date = cursor.fetchone()[0]
    cursor.close()

    if date is None:
        raise Exception(f'No message found for machine #{machine_id} in the opkald2 table!')

    delta = ref_datetime - date

    return delta.seconds
