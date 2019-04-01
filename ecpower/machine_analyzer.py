import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# machine = 1005171049
# machine = 2100102907
machine = 2000410280
limit = 1000
interval = 'W'

db = mysql.connector.connect(
    host="192.38.56.161",
    port="3306",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)

cursor = db.cursor()

cursor.execute(f'SELECT * FROM anlaegshaendelser WHERE anlaeg_id = {machine} AND haendelse = 112 LIMIT {limit};')

result = pd.DataFrame(cursor.fetchall(), columns=['id', 'dato', 'effekt', 'haendelse', 'opkald_id', 'anlaeg_id', 'opkdato', 'sortorder', 'groupId', 'admin', 'timeZone'])

print(f'Total of {len(result)} misfires for this machine found (limit {limit}).')

result['date'] = pd.to_datetime(result['dato'])

dates = result.loc[:, ['date']]
dates['size'] = pd.Series(np.full((dates.shape[0],), 50, dtype=int))
dates['misfires'] = pd.Series(np.ones((dates.shape[0],), dtype=int))

resampled = dates.resample(f'{interval}', on='date').sum()

register_matplotlib_converters()

plt.scatter(resampled.index, resampled['misfires'], s=resampled['size'], c='red')
plt.show()
