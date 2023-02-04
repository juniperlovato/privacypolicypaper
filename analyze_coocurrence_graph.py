# read a graphmal file for a weighted graph and plot zipf-ranked degree and strength distributions

import argparse

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

args = argparse.ArgumentParser()
args.add_argument('input', help='input graphml file')

args = args.parse_args()

G = nx.read_graphml(args.input)

# degree distribution

degrees_df = pd.DataFrame({'degree': [G.degree(n) for n in G.nodes()]})

degrees_df['rank'] = degrees_df['degree'].rank(ascending=False)

input_basename = args.input.split('/')[-1].split('.')[0]

plt.figure(constrained_layout=True)
plt.title('Degree distribution')
plt.ylabel('Degree')
plt.xlabel('Rank')
plt.plot(degrees_df['rank'], degrees_df['degree'], 'o', color='#2D9BF0')
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
plt.savefig(input_basename + '.strength_distribution.pdf')
plt.draw()

plt.show()
