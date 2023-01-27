# Generate a co-occurrence network from a corpus of text
#
# This script takes a CSV file with a column of text and generates a co-occurrence network
# from the text.
#
# 1. use sklearn's CountVectorizer to generate a co-occurrence matrix from the documents,
#    using our lexicon as the vocabulary
# 2. use networkx to draw a graph and generate an edge list
# 3. use third_party.backboning to generate a backbone network edgelist
# 4. Use networkx to draw the backbone network

import argparse
import os

import pandas as pd
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

import lib.pii_terms as pii
from lib.timed_execution import Timer
import third_party.backbone as bb
from lib import cooccurrence

args = argparse.ArgumentParser()
args.add_argument('input', type=str)
args.add_argument('--output_path', type=str, default='.')
args.add_argument('--no-show', action='store_true')

args = args.parse_args()

with Timer("Reading input file"):
    df = pd.read_csv(args.input)
    print("Number of rows: ", len(df))

# use our lexicon as the vocabulary
vocabulary = pii.get_list(cleaning_steps=set(['tokenize', 'downcase']))

print("Vocabulary size: {}".format(len(vocabulary)))

# use sklearn's CountVectorizer to generate a co-occurrence matrix from the documents
documents = df['policy_text'].tolist()

with Timer("Creating co-occurrence matrix"):
    cooccurrence_matrix = cooccurrence.build_matrix(documents, vocabulary)

g = nx.from_pandas_adjacency(cooccurrence_matrix)

def rescaler(values, newmin, newmax):
    oldmin = min(values)
    oldmax = max(values)
    oldrange = oldmax - oldmin
    newrange = newmax - newmin
    slope = newrange/oldrange
    offset = newmax - slope*oldmax
    return lambda x: slope*x + offset

def draw(g):
    widths = nx.get_edge_attributes(g, 'weight')
    print(f"Number of edges: {len(widths)}")
    # normalize widths
    width_values = [width for width in widths.values()]

    rescale = rescaler(width_values, 0.5, 50)

    for edge, width in widths.items():
        widths[edge] = max([rescale(width), 1])

    nodelist = g.nodes()

    plt.figure(figsize=(12,8))

    # pos = nx.kamada_kawai_layout(g)
    pos = nx.nx_pydot.pydot_layout(g)
    # pos = nx.spring_layout(g, k=10, iterations=100)
    # pos = nx.shell_layout(g)
    nx.draw_networkx_nodes(g, pos,
                        nodelist=nodelist,
                        node_size=1500,
                        node_color='grey',
                        alpha=0.7)
    nx.draw_networkx_edges(g, pos,
                        edgelist = widths.keys(),
                        width=list(widths.values()),
                        edge_color='lightblue',
                        alpha=0.6)
    nx.draw_networkx_labels(g, pos=pos,
                            labels=dict(zip(nodelist,nodelist)),
                            font_color='black')
    plt.box(False)
    plt.draw()

input_base = args.input.split('/')[-1].split('.')[0]
output_base = os.path.join(args.output_path, input_base)
nx.write_graphml(g, output_base + "-cooccurrence.graphml")

# with Timer("Drawing graph"):
#     draw(g)

def generate_backbone_graph(g, threshold):
    with Timer("Generating backbone network"):
        annotated_graph = bb.disparity_filter(g)
        backbone = bb.disparity_filter_alpha_cut(annotated_graph, alpha_t=threshold)

    return backbone

g2 = generate_backbone_graph(g, 0.5)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.5.graphml")

g2 = generate_backbone_graph(g, 0.4)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.4.graphml")

g2 = generate_backbone_graph(g, 0.3)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.3.graphml")

g2 = generate_backbone_graph(g, 0.2)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.2.graphml")

g2 = generate_backbone_graph(g, 0.1)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.1.graphml")

g2 = generate_backbone_graph(g, 0.05)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.05.graphml")

g2 = generate_backbone_graph(g, 0.01)
nx.write_graphml(g2, output_base + "-cooccurrence_backbone_0.01.graphml")

if not args.no_show:
    draw(g2)
    plt.show()
