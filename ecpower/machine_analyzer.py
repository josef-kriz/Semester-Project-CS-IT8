import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# machine_id = 1005171049
# machine_id = 2100102907
machine_id = 2000410280
db_row_limit = 1000  # limit for the number of rows being queried from the database
interval = 'W'  # resampling time interval (handbook: http://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects)
cluster_threshold = 2  # number of misfires in the interval for them to be considered as a cluster

# Define the MySQL connection
db = mysql.connector.connect(
    host="192.38.56.161",
    port="3306",
    user="chp",
    passwd="ecpower5",
    database="ecpower"
)

# Execute the query
# Get all the misfire incidents for the given machine
cursor = db.cursor()
cursor.execute(f'SELECT * FROM anlaegshaendelser WHERE anlaeg_id = {machine_id} AND haendelse = 112 LIMIT {db_row_limit};')

# Turn the result into a pandas DataFrame
result = pd.DataFrame(cursor.fetchall(), columns=['id', 'dato', 'effekt', 'haendelse', 'opkald_id', 'anlaeg_id', 'opkdato', 'sortorder', 'groupId', 'admin', 'timeZone'])

print(f'Total of {len(result)} misfires for this machine found (limit {db_row_limit}).')

# Create a new column with the date in correct format
result['date'] = pd.to_datetime(result['dato'])

# Create a new DataFrame using the new date column from result
# put 1 for misfire count and default dot size of 50
dates = result.loc[:, ['date']]
dates['size'] = pd.Series(np.full((dates.shape[0],), 50, dtype=int))
dates['misfires'] = pd.Series(np.ones((dates.shape[0],), dtype=int))

# resample the dates dataframe according to the given interval
resampled = dates.resample(interval, on='date').sum()

# get all rows with misfire count greater than cluster_threshold
nonzero = resampled[(resampled.T != 0).any()]
nonzero = nonzero.loc[nonzero['misfires'] >= cluster_threshold]

print(f'Total of {len(nonzero)} clusters found where at least {cluster_threshold} happened in {interval}')

register_matplotlib_converters()

plt.scatter(resampled.index, resampled['misfires'], s=resampled['size'], c='red')
plt.show()
