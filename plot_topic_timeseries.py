import argparse

import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.kaleido.scope.mathjax = None

parser = argparse.ArgumentParser()
parser.add_argument('topic_prevalence_file', help='Input CSV file with topic prevalence over time')

args = parser.parse_args()

topic_metrics = pd.read_csv(args.topic_prevalence_file, index_col=0, sep=',', quotechar='"')

for col in topic_metrics.columns:
    print(col)

# create list of topic names sorted by average prevalence of the topic over time
topic_names = topic_metrics.mean().sort_values(ascending=False).index

# reorder columns accordingly
topic_metrics = topic_metrics[topic_names]

# normalize topics to sum to 1
topic_metrics = topic_metrics.div(topic_metrics.sum(axis=1), axis=0)

# determine number of topics in each group
num_topics_per_group = len(topic_names) // 3

# determine which topics are in each group
top_topics = topic_names[:num_topics_per_group]
middle_topics = topic_names[num_topics_per_group:2*num_topics_per_group]
bottom_topics = topic_names[2*num_topics_per_group:]

# create list of line styles for each topic
line_styles = []
for topic in topic_names:
    if topic in top_topics:
        line_styles.append('solid')
    elif topic in middle_topics:
        line_styles.append('dash')
    elif topic in bottom_topics:
        line_styles.append('dot')

# list of 6 easily distinguished colors
color_map = ['#FFB14E', '#EA5F94', '#2D9BF0', '#6FEA5F', '#B14EFF', '#5FF0EA']


# shorten color map to group size and repeat for each group
color_map = [color_map[:len(group)] for group in [top_topics, middle_topics, bottom_topics]]
color_map = [color for group in color_map for color in group]

# plot
fig = px.line(topic_metrics, title='Topic prevalence over time',
    labels={'index': 'Year', 'value': 'Prevalence', 'variable': 'Topic'},
    color_discrete_map={topic: color_map[i] for i, topic in enumerate(topic_names)})

# use Arial font, black, 14pt
fig.update_layout(font=dict(family='Arial', color='#000000', size=14))

# set line styles
for i, trace in enumerate(fig.data):
    trace.line.dash = line_styles[i]

fig.write_image("topics_over_time.pdf", width=900, height=600)

# fig.show()
