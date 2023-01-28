# compare two topics by first creating a superset of all words in the two topics
# then create a vector for each topic with the word counts, filling in 0 for words that are not in the topic
# then compute the cosine similarity between the two vectors

from typing import List, Tuple, Dict, NamedTuple, Callable, Optional, Set
from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cosine

Representation = List[Tuple[str, float]]

def make_comparable(representations: List[Representation]) -> List[Representation]:
    # clone the representations so we can modify them
    representations = [r[:] for r in representations]

    # create a superset of all words in all the representations
    words = set()
    for representation in representations:
        words.update([w for w, _ in representation])

    for representation in representations:
        for word in words:
            if word not in [word for word, score in representation]:
                representation.append((word, 0))
    for representation in representations:
        representation.sort(key=lambda x: x[0])

    assert all(len(representation) == len(words) for representation in representations)
    return representations

def compare_topics(topic1: Representation, topic2: Representation) -> float:
    topic1, topic2 = make_comparable([topic1, topic2])
    count_vector1 = np.array([c for _, c in topic1])
    count_vector2 = np.array([c for _, c in topic2])
    return float(1 - cosine(count_vector1, count_vector2))

class ScoredMatch(NamedTuple):
    topic_id: int
    similarity: float
Strategy = Callable[[List[Representation]], Representation]

latest_strategy: Strategy = lambda representations: representations[-1]
first_strategy: Strategy = lambda representations: representations[0]
def average_representations(representations: List[Representation]) -> Representation:
    assert len(representations) > 0

    if len(representations) == 1:
        return representations[0]

    representations = make_comparable(representations)

    # average the scores for each word
    words = [word for word, _ in representations[0]]
    scores = np.array([0.0 for _ in words])
    for representation in representations:
        scores += np.array([score for _, score in representation])
    scores = scores / len(representations)

    return list(zip(words, scores))
average_strategy: Strategy = average_representations

class KnownTopics:
    def __init__(self,
                 strategy: Strategy = latest_strategy,
                 threshold: float = 0.5):
        self.topic_dict: Dict[int, List[Representation]] = {}
        self.strategy = strategy
        self.threshold = threshold

    def topics(self) -> List[List[Representation]]:
        return list(self.topic_dict.values())

    # TODO: Currently this can match multiple new topics to the same old topic
    #       Think about whether this is a problem
    def add_topics(self, topics: List[Representation]) -> Tuple[Dict[int, Representation], List[int]]:
        new_overall_topic_dict = self.topic_dict.copy()
        these_topics = {}

        # this can match multiple new topics to the same old topic
        # record when that happens

        new_matches = defaultdict(list)

        for topic in topics:
            best_match = self.find_best_match(topic)
            if best_match is None or best_match.similarity < self.threshold:
                # new global topic
                topic_id = len(new_overall_topic_dict)
                new_overall_topic_dict[topic_id] = [topic]
            else:
                # It's a match!
                topic_id = best_match.topic_id
                new_overall_topic_dict[topic_id].append(topic)
                new_matches[topic_id].append((best_match.similarity, topic))
            these_topics[topic_id] = topic

        # find the topics that were matched to multiple new topics
        group_matches = {id:matches for id, matches in new_matches.items() if len(matches) > 1}
        if len(group_matches) > 0:
            print("!!!!!!MULTI-MATCH WARNING!!!!!!!")
        for id, matches in group_matches.items():
            print(f"Multiple new topics matched to old topic {id}:")
            for match in matches:
                print(f"  {match[0]}: {match[1]}")

        matched_topic_ids = [id for id in these_topics.keys() if id in self.topic_dict.keys()]

        self.topic_dict = new_overall_topic_dict

        return these_topics, matched_topic_ids

    def find_best_match(self,
                        new_topic: Representation,
                        strategy: Optional[Strategy] = None) -> Optional[ScoredMatch]:
        if strategy is None:
            strategy = self.strategy
        best_match: Optional[ScoredMatch] = None
        for topic_id, representations in self.topic_dict.items():
            similarity = compare_topics(strategy(representations), new_topic)
            if best_match is None or similarity > best_match.similarity:
                best_match = ScoredMatch(topic_id, similarity)
        return best_match
