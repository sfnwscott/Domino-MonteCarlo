import pandas as pd
import matplotlib.pyplot as plt
import itertools

# df = pd.read_csv('results_all_min.csv')#,index_col='Unnamed: 0')
# grouped = df.groupby('game num')
# lastrounds = grouped.last()
# grouped_rounds = df.groupby('round num')

# print(df['round num'].value_counts())

print(len(list(itertools.combinations_with_replacement(['3','4','5','6','7'],2))))