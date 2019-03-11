import pandas as pd
import numpy

opkald2 = pd.read_csv('<PATH_TO_CSV_FILE>',
                      delimiter='\t',
                      encoding='ISO-8859-1',
                      na_values=[
                          '\\N',
                          'ABSENT',
                          'ERRORS'
                      ],
                      dtype={
                          'debug_info': str
                      }
                      )


def parse_debug_info():
    for row in opkald2['debug_info']:
        if row not in [numpy.NaN, '00000000000000000000000000000000000000000', '000000000000000000000000000000000000']:
            print('\t', row)


opkald2['dateCreated'] = pd.to_datetime(opkald2['dateCreated'])
opkald2['opkdato'] = pd.to_datetime(opkald2['opkdato'])

# print(opkald2.head())
# print(opkald2.iloc[:, 53])

print('Standard deviations for numeric columns (column name, value):')
for column in opkald2:
    if opkald2[column].dtype == 'int64' or opkald2[column].dtype == 'float64':
        print(column)
        print('\t min:', opkald2[column].min())
        print('\t max:', opkald2[column].max())
        # print('\t mod:', opkald2[column].mode().to_list()[0], '(out of ', len(opkald2[column].mode().to_list()), ')')
        print('\t avg:', opkald2[column].mean())
        print('\t std:', opkald2[column].std())

print('Non-zero values for debug_info:')
parse_debug_info()
