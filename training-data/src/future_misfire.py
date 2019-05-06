from .chpdb import cursor


#Returns true if there is a misfire
def check_for_future_misfire(date, machineID, interval):
    query = "SELECT COUNT(1) " \
            "FROM anlaegshaendelser " \
            "WHERE misfire_shutdown = 1 " \
            "AND anlaeg_id = {} " \
            "AND opkdato > {} " \
            "AND opkdato < {};".format(machineID, date, date + interval)
    cursor.execute(query)
    return cursor.fetchone() != 0