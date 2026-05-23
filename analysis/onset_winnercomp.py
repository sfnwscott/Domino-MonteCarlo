import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
colors = ['tab:blue','tab:red','tab:green']
filenames = ['results_mixed_oddmax_evenmin.csv', 'results_mixed_oddmax_evenminoptions.csv', 
             'results_mixed_oddmin_evenminoptions.csv']
labels = ['Minimize Board Total', 'Minimize Board Options', 'Maximize Tile Sum']
#for i in range(3):
i = 1
df = pd.read_csv(filenames[i])
ct1 = pd.crosstab(df['started on set'], df['went out first'])
ct = pd.crosstab(df['started on set'], df['went out first'], normalize='index')
arr = ct.to_numpy()
arr = arr[:,1:]
diag_arr = np.diag(arr)
avg_pct = np.mean(np.diag(arr)) * 100
std_pct = np.std(np.diag(arr)) * 100
print(ct1)
print(ct*100)
print(diag_arr*100)
print(avg_pct)
print(std_pct)
print('')



# filenames = ['results_all_min.csv', 'results_all_minoptions.csv', 'results_all_max.csv']

# for i in range(3):

#     df = pd.read_csv(filenames[i])
#     ct1 = pd.crosstab(df['started on set'], df['went out first'])
#     ct = pd.crosstab(df['started on set'], df['went out first'], normalize='index')
#     arr = ct.to_numpy()
#     arr = arr[:,1:]

#     avg_pct = np.mean(np.diag(arr)) * 100
#     std_pct = np.std(np.diag(arr)) * 100
#     print(avg_pct)
#     print(std_pct)
#     print('')

#ct['pct matching'] = 


# sns.heatmap(ct, annot=True, cmap='magma')
# plt.show()
#print(ct.mean(axis=0))
# result = list(stats.chi2_contingency(ct))
# print(result[0])



# i=0
# df = pd.read_csv(filenames[i])#,index_col='Unnamed: 0')
# df['point sum'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].sum(axis=1)
# df['mean round score'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].mean(axis=1)
# grouped = df.groupby('game num')
# lastrounds = grouped.last()
# lastrounds['team odd pts'] = lastrounds['player1 pts'] + lastrounds['player3 pts']
# lastrounds['team even pts'] = lastrounds['player2 pts'] + lastrounds['player4 pts']
# num_games = lastrounds.shape[0]
# odd_wincount = (lastrounds['team odd pts'] > lastrounds['team even pts']).sum()
# frac_oddwin = odd_wincount / num_games
# pct_oddwin = frac_oddwin * 100
# frac_evenwin = 1 - frac_oddwin
# pct_evenwin = frac_evenwin * 100
# print(df.columns)
# print(df['started on set'])
# #print(df['started on set'].corr(df['went out first']))
# ct = pd.crosstab(df['started on set'], df['went out first'])
# # sns.heatmap(ct, annot=True, cmap='magma')
# # plt.show()
# result = list(stats.chi2_contingency(ct))

# print(result[1])
