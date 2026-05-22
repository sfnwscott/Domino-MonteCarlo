import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(
    nrows = 1, ncols=1, figsize=(12,8)#, gridspec_kw={'height_ratios': [3,1]}
)
colors = ['tab:blue','tab:red','tab:green']
filenames = ['results_dynamic_oddminmax_evenmax.csv', 
             'results_dynamic_oddminmax_evenmin.csv', 
             'results_dynamic_oddminmax_evenminoptions.csv']
labels = ['Minimize Board Total', 'Minimize Board Options', 'Maximize Tile Sum']
for i in range(3):

    df = pd.read_csv(filenames[i])#,index_col='Unnamed: 0')
    df['point sum'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].sum(axis=1)
    df['mean round score'] = df[['player1 pts','player2 pts', 'player3 pts', 'player4 pts']].mean(axis=1)
    grouped = df.groupby('game num')
    lastrounds = grouped.last()
    lastrounds['team odd pts'] = lastrounds['player1 pts'] + lastrounds['player3 pts']
    lastrounds['team even pts'] = lastrounds['player2 pts'] + lastrounds['player4 pts']
    num_games = lastrounds.shape[0]
    odd_wincount = (lastrounds['team odd pts'] > lastrounds['team even pts']).sum()
    frac_oddwin = odd_wincount / num_games
    pct_oddwin = frac_oddwin * 100
    frac_evenwin = 1 - frac_oddwin
    pct_evenwin = frac_evenwin * 100
    if i == 0:
        col = 'tab:purple'
        label = 'Dynamic On Set'
        ax.bar((i+1)*1.1, pct_oddwin, color=col, label=label, width=0.2, align='center')
        col = colors[2]
        label = labels[2]
        ax.bar((i+1)*1.1 + 0.2, pct_evenwin, color=col, label=label, width=0.2, align='center')
    if i == 1:
        col = 'tab:purple'
        label = labels[2]
        ax.bar((i+1)*1.1, pct_oddwin, color=col, width=0.2, align='center')
        col = colors[0]
        label = labels[0]
        ax.bar((i+1)*1.1 + 0.2, pct_evenwin, color=col, label=label, width=0.2, align='center')
    elif i == 2:
        col = 'tab:purple'
        label = labels[0]
        ax.bar((i+1)*1.1, pct_oddwin, color=col, width=0.2, align='center')
        col = colors[1]
        label = labels[1]
        ax.bar((i+1)*1.1 + 0.2, pct_evenwin, color=col, label=label, width=0.2, align='center')
    print(pct_oddwin)
    print(pct_evenwin)
ax.legend()
ax.set_xlim(1.1-0.5, 4.0)
#ax.set_ylim(0,60)
ax.set_xticks([1.1,1.3,2.2,2.4,3.3,3.5])
ax.set_xticklabels(['Team 1', 'Team 2', 'Team 1', 'Team 2', 'Team 1', 'Team 2'])
ax.set_ylabel('% of Games Won')
#axs[1].set_xticks(list(range(1,17)))
# axs[0].grid(True, which='both',linestyle=':',linewidth=1.0,alpha=0.75)
# axs[1].grid(True, which='both',linestyle=':',linewidth=1.0,alpha=0.75)
# axs[1].set_xlabel('Round Number')
# axs[0].set_ylabel('Average Points per Player')
# axs[1].set_ylabel('Number of Games\nReaching Round')
fig.suptitle('Dynamic Strategy Matchup Comparison')
fig.tight_layout()
plt.savefig('team_comp_dynamic.png')
plt.show()




i = 0
df = pd.read_csv(filenames[i])
print(df['went out first'].value_counts())
grouped = df.groupby('game num')
lastrounds = grouped.last()
lastrounds['team odd pts'] = lastrounds['player1 pts'] + lastrounds['player3 pts']
lastrounds['team even pts'] = lastrounds['player2 pts'] + lastrounds['player4 pts']
num_games = lastrounds.shape[0]
odd_wincount = (lastrounds['team odd pts'] > lastrounds['team even pts']).sum()
frac_oddwin = odd_wincount / num_games
pct_oddwin = frac_oddwin * 100
frac_evenwin = 1 - frac_oddwin
pct_evenwin = frac_evenwin * 100
# plt.bar(x=1, height=pct_oddwin)
# plt.show()
