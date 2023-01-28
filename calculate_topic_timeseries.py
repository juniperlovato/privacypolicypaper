# read a topics_over_time file and plot the topics over time

import argparse
from typing import List
from ast import literal_eval
import math
import json
import re

import matplotlib.pyplot as plt
import pandas as pd

import lib.compare_topics as ct
from lib.timed_execution import Timer

# file format: CSV
#   columns: topic_ids
#   rows: file names
#   cells: topic representation
# example row:
#  data/topics/1997_topics.txt,"[['address', 0.23076923076923078], ['name', 0.19230769230769232], ['family', 0.07692307692307693], ['condition', 0.07692307692307693], ['preferences', 0.07692307692307693], ['interests', 0.07692307692307693], ['employment', 0.07692307692307693], ['cookies', 0.038461538461538464], ['medicine', 0.038461538461538464], ['sex', 0.038461538461538464], ['child', 0.038461538461538464], ['behavior', 0.038461538461538464]]",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

parser = argparse.ArgumentParser()
parser.add_argument('topic_representations', help='Input CSV file containing topic representations (over time unless -s is set)')
parser.add_argument('output', help='Output file path')
parser.add_argument('-s', '--single-topic-representation', action='store_true', help='Expect only a single representation for each topic in input file')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional information')

# for each year, one CSV file with the corpus
parser.add_argument('corpus', nargs='+', help='Input CSV file with the corpus, needs to match number of years in topics_over_time')

args = parser.parse_args()

# read the topic representations
if args.single_topic_representation:
    with open(args.topic_representations) as f:
        topics = json.load(f)

    # set debugger breakpoint here to inspect topics
    # import pdb; pdb.set_trace()

    # extract years from corpus file names, the first 4-digit number is the year. Use Regex
    years = sorted([int(re.search(r'\d{4}', corpus_file).group()) for corpus_file in args.corpus])

    # create a dataframe with the topic representations so they are the same in each year
    topics_over_time = pd.DataFrame({topic_id: [topics[topic_id]] for topic_id in topics}, index=years)
    print(topics_over_time)
else:
    topics_over_time = pd.read_csv(args.topic_representations, index_col=0, sep=',', quotechar='"')

    if not len(args.corpus) == len(topics_over_time):
        raise ValueError(f'Number of corpus files ({len(args.corpus)}) does not match number of years in topics_over_time ({len(topics_over_time)})')

    # convert the topic representations from strings to lists
    for column in topics_over_time.columns:
        topics_over_time[column] = topics_over_time[column].apply(lambda x: literal_eval(x) if not pd.isna(x) else x)

    years = [path.split('/')[-1].split('_')[0] for path in topics_over_time.index]

    # change dataframe index to years
    topics_over_time.index = years

# determine topic names by averaging all representations for a topic and choosing the top 3 words
topic_names = {}
for topic_id in topics_over_time.columns:
    representations: List[ct.Representation] = list(topics_over_time[topic_id].dropna())
    if len(representations) == 0:
        continue
    average = ct.average_representations(representations)
    sorted_average = sorted(average, key=lambda x: x[1], reverse=True)
    topic_names[topic_id] = '-'.join([word for word, _ in sorted_average[:3]])
    if args.verbose:
        # print average representation
        # omit words with weight < 0.001, sort words by weight
        print(f'{topic_names[topic_id]}: {", ".join([f"{word} ({math.floor(weight*1000)/1000})" for word, weight in sorted_average if weight > 0.001])}')

# assert topic names are unique
duplicated_topic_names = [name for name in topic_names.values() if list(topic_names.values()).count(name) > 1]
assert len(duplicated_topic_names) == 0, "Topic names are not unique: " + str(duplicated_topic_names)

# compute topic prevalence for each topic for each year
# the year is determined by the file name
# the prevalence is the relative frequency of each word from the topic representation in an underlying corpus,
#   weighted by the weight from the topic representation

with Timer("Reading year corpi"):
    year_corpi = {}
    for year, corpus in zip(years, args.corpus):
        year_corpi[year] = pd.read_csv(corpus)["PII_Extracted"].apply(lambda x: x.lower())

topic_prevalence = pd.DataFrame(index=years, columns=list(topic_names.keys()))

with Timer("Computing topic prevalence"):
    for year, corpus in list(year_corpi.items()):
        total_word_count = corpus.str.split().str.len().sum()
        print(f'Year {year}: {total_word_count} words in corpus')
        for topic_id, topic_name in topic_names.items():
            topic_representation = topics_over_time.loc[year, topic_id]
            print(f'Computing prevalence for {topic_name} in {year}')
            if topic_representation == topic_representation: # improvised NaN check
                print("topic exists")
                for word, weight in topic_representation:
                    word_count = corpus.str.contains(word).sum()
                    if not pd.isna(topic_prevalence.loc[year, topic_id]):
                        topic_prevalence.loc[year, topic_id] = topic_prevalence.loc[year, topic_id] + word_count * weight
                    else:
                        topic_prevalence.loc[year, topic_id] = word_count * weight
                print(f'Prevalence for {topic_name} in {year}: {topic_prevalence.loc[year, topic_id]/total_word_count}')
            else:
                print("topic doesn't exist")
                topic_prevalence.loc[year, topic_id] = 0
        topic_prevalence.loc[year] = topic_prevalence.loc[year] / total_word_count

# replace column names with topic names
topic_prevalence.columns = [topic_names[topic_id] for topic_id in topic_prevalence.columns]

print(topic_prevalence)

# dump topic prevalence to CSV
topic_prevalence.to_csv(args.output)
