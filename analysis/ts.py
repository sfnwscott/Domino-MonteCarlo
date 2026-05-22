import pandas as pd
import matplotlib.pyplot as plt
import os


df = pd.read_csv('results_mixed_strategies.csv')#,index_col='Unnamed: 0')
grouped = df.groupby('game num')
lastrounds = grouped.last()
grouped_rounds = df.groupby('round num')

colors = ['tab:blue','tab:red','tab:purple','tab:brown']

fig = plt.figure(1)
# ax = fig.add_subplot(1,4,1)
# for i in range(4):
#     col = colors[i]
#     label = f'Player {i+1}'
#     means = grouped_rounds[f'player{i+1} pts'].mean()
#     stds = grouped_rounds[f'player{i+1} pts'].std()
#     # print(means)
#     # print(grouped_rounds.groups.keys())
#     #ax.scatter(df['round num'], df[f'player{i+1} pts'], color=col,label=label)
#     ax.errorbar(grouped_rounds.groups.keys(), means, yerr=stds, color=col,label=label)
#     # print(label)
#     # print(f'Mean points: {column.mean()}')
#     # print(f'Standard deviation: {column.std()}')
#     #print('')
# ax.set_title('Strategy: Mixed')
# ax.set_xlim(0,7)
# ax.set_ylim(0,30)
# ax.set_xlabel('Round Number')
# ax.set_ylabel('Points')
# ax.legend()

# print(grouped_rounds.size())



df = pd.read_csv('results_all_min.csv')#,index_col='Unnamed: 0')
grouped = df.groupby('game num')
lastrounds = grouped.last()
grouped_rounds = df.groupby('round num')

colors = ['tab:blue','tab:red','tab:purple','tab:brown']


#fig = plt.figure(2)
ax = fig.add_subplot(1,3,1)
for i in range(4):
    col = colors[i]
    label = f'Player {i+1}'
    means = grouped_rounds[f'player{i+1} pts'].mean()
    stds = grouped_rounds[f'player{i+1} pts'].std()
    # print(means)
    # print(grouped_rounds.groups.keys())
    #ax.scatter(df['round num'], df[f'player{i+1} pts'], color=col,label=label)
    ax.errorbar(grouped_rounds.groups.keys(), means, yerr=stds, color=col,label=label)
    # print(label)
    # print(f'Mean points: {column.mean()}')
    # print(f'Standard deviation: {column.std()}')
    #print('')
ax.legend()
ax.set_xlim(0,7)
ax.set_ylim(0,30)
ax.set_xlabel('Round Number')
ax.set_ylabel('Points')
ax.set_title('Strategy: Minimize Board Count')

print(grouped_rounds.size())


df = pd.read_csv('results_all_max.csv')#,index_col='Unnamed: 0')
grouped = df.groupby('game num')
lastrounds = grouped.last()
grouped_rounds = df.groupby('round num')

colors = ['tab:blue','tab:red','tab:purple','tab:brown']


#fig = plt.figure(3)
ax = fig.add_subplot(1,3,2)
for i in range(4):
    col = colors[i]
    label = f'Player {i+1}'
    means = grouped_rounds[f'player{i+1} pts'].mean()
    stds = grouped_rounds[f'player{i+1} pts'].std()
    # print(means)
    # print(grouped_rounds.groups.keys())
    #ax.scatter(df['round num'], df[f'player{i+1} pts'], color=col,label=label)
    ax.errorbar(grouped_rounds.groups.keys(), means, yerr=stds, color=col,label=label)
    # print(label)
    # print(f'Mean points: {column.mean()}')
    # print(f'Standard deviation: {column.std()}')
    #print('')
ax.set_xlim(0,7)
ax.set_ylim(0,30)
ax.set_xlabel('Round Number')
ax.set_ylabel('Points')
ax.legend()
ax.set_title('Strategy: Maximize Tile Count Removal')
print(grouped_rounds.size())



df = pd.read_csv('results_all_minoptions.csv')#,index_col='Unnamed: 0')
grouped = df.groupby('game num')
lastrounds = grouped.last()
grouped_rounds = df.groupby('round num')

colors = ['tab:blue','tab:red','tab:purple','tab:brown']


#fig = plt.figure(3)
ax = fig.add_subplot(1,3,3)
for i in range(4):
    col = colors[i]
    label = f'Player {i+1}'
    means = grouped_rounds[f'player{i+1} pts'].mean()
    stds = grouped_rounds[f'player{i+1} pts'].std()
    # print(means)
    # print(grouped_rounds.groups.keys())
    #ax.scatter(df['round num'], df[f'player{i+1} pts'], color=col,label=label)
    ax.errorbar(grouped_rounds.groups.keys(), means, yerr=stds, color=col,label=label)
    # print(label)
    # print(f'Mean points: {column.mean()}')
    # print(f'Standard deviation: {column.std()}')
    #print('')
ax.set_xlim(0,7)
ax.set_ylim(0,30)
ax.set_xlabel('Round Number')
ax.set_ylabel('Points')
ax.legend()
ax.set_title('Strategy: Minimize Options for Next Player')
print(grouped_rounds.size())
plt.show()
# fig = plt.figure(2)
# ax = fig.add_subplot(1,1,1)
# for i in range(4):
#     col = colors[i]
#     label = f'Player {i+1}'
#     column = lastrounds[f'player{i+1} pts'].values
#     ax.hist(column, bins=5, color=col, edgecolor='black',label=label)
#     print(label)
#     print(f'Mean points: {column.mean()}')
#     print(f'Standard deviation: {column.std()}')
#     print('')
# ax.legend()
# plt.show()

# ax.