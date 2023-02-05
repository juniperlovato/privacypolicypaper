# read a graphmal file for a weighted graph and plot zipf-ranked degree and strength distributions

import argparse

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np

args = argparse.ArgumentParser()
args.add_argument('input', help='input graphml file')

args = args.parse_args()

G = nx.read_graphml(args.input)

# degree distribution

degrees_df = pd.DataFrame({'degree': [G.degree(n) for n in G.nodes()]})

degrees_df['rank'] = degrees_df['degree'].rank(ascending=False)

input_basename = args.input.split('/')[-1].split('.')[0]

fig = plt.figure(constrained_layout=True)
plt.title('Degree distribution')
plt.ylabel('Degree')
plt.xlabel('Rank')
plt.plot(degrees_df['rank'], degrees_df['degree'], 'o', color='#2D9BF0')

linear_regime = degrees_df[degrees_df['rank'] < 175]
linear_regime = linear_regime.sort_values(by='rank')
max_rank = degrees_df['rank'].max()

# add regression line to linear plot, extend to the right
slope, intercept, r_value, p_value, std_err = stats.linregress(linear_regime['rank'], linear_regime['degree'])
plt.plot([0, max_rank], [intercept, slope*max_rank + intercept], color='#EA5F94')

plt.savefig(input_basename + '.degree_distribution.pdf')
plt.draw()

# strength distribution
strengths_df = pd.DataFrame({'strength': [G.degree(n, weight='weight') for n in G.nodes()]})

strengths_df['rank'] = strengths_df['strength'].rank(ascending=False)

plt.figure(constrained_layout=True)
plt.title('Strength distribution')
plt.ylabel('Strength')
plt.xlabel('Rank')
plt.semilogy(strengths_df['rank'], strengths_df['strength'], 'o', color='#2D9BF0')

low = 25
high = 200
linear_regime = strengths_df[(strengths_df['rank'] >= low) & (strengths_df['rank'] <= high)]
linear_regime = linear_regime.sort_values(by='rank')
max_rank = degrees_df['rank'].max()

# add regression line to linear plot, extend to the right
# Careful: this is a plot with logarithmic y-axis and linear x-axis
slope, intercept, r_value, p_value, std_err = stats.linregress(linear_regime['rank'], np.log10(linear_regime['strength']))
plt.plot([0, max_rank], [10**intercept, 10**(intercept+slope*max_rank)], color='#EA5F94')

plt.savefig(input_basename + '.strength_distribution.pdf')
plt.draw()

plt.show()
