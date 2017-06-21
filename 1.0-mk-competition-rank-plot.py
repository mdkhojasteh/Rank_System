
# coding: utf-8

# # Competitions
# ## Import useful librarries

# In[2]:

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython import get_ipython
get_ipython().magic('matplotlib inline')


# ## Import CSV file

# In[3]:

data = pd.read_csv('../data/raw/submissions.csv').dropna()


# In[4]:

data.head()


# In[5]:

competitions = pd.read_csv('../data/raw/competitions.csv').dropna()
competitions


# In[6]:

s = pd.to_datetime(data.timestamp.min())
week = []
for i in data.timestamp:
    week.append(int(((pd.to_datetime(i) - s).days)/7))
data['week'] = week


def plot_competition_graph(competition_id, sort_ascending, title):
    if competition_id == 3:
        print('No competition')
    else:
        com = data[data.competition_id == competition_id]
        lb = pd.DataFrame(index=com.user_id.unique())
        lb['best_score'] = 0
        weeks = com.week.unique()
        weeks.sort()
        for week in weeks:
            this_week = com[com.week == week]
            if sort_ascending:
                best_this_week = this_week.groupby(
                    'user_id').score.min().to_frame()
            else:
                best_this_week = this_week.groupby(
                    'user_id').score.max().to_frame()
            mask = lb.loc[best_this_week.index, :].max(
                axis=1) < best_this_week.score
            best_this_week.columns = ['best_week_{}'.format(week)]
            lb = lb.join(best_this_week[mask])
        lb = lb.fillna(method='ffill', axis=1)
        lb.drop('best_score', axis=1, inplace=True)
        lb[lb == 0] = np.nan
        lb = pd.Series.rank(lb, method='first')
        lb['Ranks'] = lb[lb.columns[-1]]
        first = lb[lb.Ranks == 1].index
        a = np.where(lb.index == first[0])
# Plotting
        ax = lb.T.plot(figsize=(40, 15), legend=False, alpha=0.3,
                       linewidth=4)
        for i in range(1, 26):
            ax.set_yticks(range(1, 26))
        labels = [("Week %d" % week) for week in weeks]
        plt.xticks(np.arange(len(lb.columns)), labels)
        ax.yaxis.tick_right()
        plt.ylim(0, 25.5)
        plt.gca().invert_yaxis()
        plt.grid(b=False)
        plt.title(title, size=20, weight='bold')
        ax.annotate('', xy=(0, 0), xytext=(0, 27),
                    arrowprops=dict(facecolor='black',
                    arrowstyle="-", linewidth=4))
        ax.annotate('', xy=(len(lb.columns)-2, 0),
                    xytext=(len(lb.columns)-2, 27),
                    arrowprops=dict(facecolor='black',
                    arrowstyle="-", linewidth=4))
        ax.annotate("Low", xy=(0, 25.5), xycoords="data",
                    xytext=(-0.1, 25.5), size=20, ha="right",
                    bbox=dict(boxstyle="round", fc="w"))
        ax.annotate("High", xy=(0, 0.45), xycoords="data",
                    size=20, xytext=(-0.1, 0.45), ha="right",
                    bbox=dict(boxstyle="round", fc="w"))
        ax.annotate("Ranking", xy=(0, 12.75), xycoords="data",
                    weight='bold', size=20,
                    xytext=(-0.1, 12.75), ha="right",
                    bbox=dict(boxstyle="round", fc="w"))
        ax.annotate("Finish", xy=(len(lb.columns)-1, 25.5),
                    xycoords="data", weight='bold',
                    size=23, xytext=(len(lb.columns)-1, 27),
                    ha="left",
                    bbox=dict(boxstyle="round", fc="w"))
        ax.annotate("Start", xy=(0, 25.5), xycoords="data",
                    weight='bold', size=23, xytext=(0.1, 27),
                    ha="left", bbox=dict(boxstyle="round", fc="w"))
        ax.lines[a[0]].set_linewidth(10)
        plt.savefig('../reports/figures/%s.png' % title)


# In[7]:

for competition_id, sort, title in zip(
    competitions.competition_id,
        competitions.sort_ascending, competitions.title):
    plot_competition_graph(competition_id, sort, title)

