import pandas as pd

df = pd.read_csv('output/wrapper_test_2.csv')

top_five = df.sort_values('recall', ascending=False).head(5)

for i in top_five.values:
    print(i)