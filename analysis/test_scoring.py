import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# fig = plt.figure(1, figsize=(10,8), dpi=100)
# ax = fig.add_subplot(1,1,1)
# fig, axs = plt.subplot_mosaic(
#     [['main'], ['roundcounts']],

# )
fig, axs = plt.subplots(
    nrows = 2, ncols=1, figsize=(12,8),sharex=True, gridspec_kw={'height_ratios': [3,1]}
)
colors = ['tab:blue','tab:red','tab:green']
filenames = ['results_all_min.csv', 'results_all_minoptions.csv', 'results_all_max.csv']
labels = ['Minimize Board Total', 'Minimize Board Options', 'Maximize Tile Sum',]
for i in range(3):
    df = pd.read_csv(filenames[i])#,index_col='Unnamed: 0')
    df['point sum'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].sum(axis=1)
    df['mean round score'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].mean(axis=1)
    grouped_rounds = df.groupby('round num')
    mean_pts = grouped_rounds['mean round score'].mean()
    std_pts = grouped_rounds['mean round score'].std()
    col = colors[i]
    label = labels[i]
    x_vals = np.array(list(grouped_rounds.groups.keys()))
    x_vals = x_vals + 0.1*(i - 1)
    axs[0].errorbar(x_vals, mean_pts, yerr=std_pts, capsize=3, color=col,label=label)
    round_counts = df['round num'].value_counts()
    axs[1].plot(x_vals, round_counts, color=col, label=label)
axs[0].legend()
axs[1].set_xlim(0.5, 16.5)
axs[0].set_ylim(0,60)
axs[1].set_ylim(0,600)
axs[1].set_xticks(list(range(1,17)))
axs[0].grid(True, which='both',linestyle=':',linewidth=1.0,alpha=0.75)
axs[1].grid(True, which='both',linestyle=':',linewidth=1.0,alpha=0.75)
axs[1].set_xlabel('Round Number')
axs[0].set_ylabel('Average Points per Player')
axs[1].set_ylabel('Number of Games\nReaching Round')
fig.suptitle(f'Strategy Point Scoring Comparison (N={df['game num'].value_counts().shape[0]})')
fig.tight_layout()
plt.savefig('strat_comp.png')
plt.show()
    




print(df)

