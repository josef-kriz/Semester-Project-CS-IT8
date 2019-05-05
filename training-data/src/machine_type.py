from .chpdb import cursor


# Returns list of discretized machine types of order [6, 9, 13, 17, 19, 20, 9-FORD, 17BIO}.
def get_machine_type(machine_id):
    type_list = [0, 0, 0, 0, 0, 0, 0, 0]

    cursor.execute(f'SELECT effekt FROM anlaeg WHERE anlaegnr = {machine_id};')
    effekt = cursor.fetchone()[0]

    if effekt is None:
        raise Exception(f'Machine #{machine_id} was not found in the anlaeg table!')
    elif effekt == '':
        raise Exception(f'Machine #{machine_id} has no effekt in the anlaeg table!')
    elif effekt == 'XRGI® 6':
        type_list[0] = 1
    elif effekt == 'XRGI® 9':
        type_list[1] = 1
    elif effekt == 'XRGI® 13':
        type_list[2] = 1
    elif effekt == 'XRGI® 17':
        type_list[3] = 1
    elif effekt == 'XRGI® 19':
        type_list[4] = 1
    elif effekt == 'XRGI® 20':
        type_list[5] = 1
    elif effekt == 'XRGI® 9-FORD':
        type_list[6] = 1
    elif effekt == 'XRGI® 17BIO':
        type_list[7] = 1

    print(type_list)

    return type_list