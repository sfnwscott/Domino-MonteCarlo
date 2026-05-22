import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('results_all_combos.csv')
print(df.columns)
#grouped = df.groupby('game num')
lastrounds = df.groupby(['team-1 strategy','team-2 strategy','game num']).last()
lastrounds['team odd pts'] = lastrounds['player1 pts'] + lastrounds['player3 pts']
lastrounds['team even pts'] = lastrounds['player2 pts'] + lastrounds['player4 pts']
num_games = lastrounds.shape[0]
odd_wincount = (lastrounds['team odd pts'] > lastrounds['team even pts']).sum()
frac_oddwin = odd_wincount / num_games
pct_oddwin = frac_oddwin * 100
frac_evenwin = 1 - frac_oddwin
pct_evenwin = frac_evenwin * 100
#ct = pd.crosstab(df['team-1 strategy'],df['team-2 strategy'],values=)
print(lastrounds[])