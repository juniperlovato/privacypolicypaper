import pytest
from math import sqrt

import lib.compare_topics as ct

def test_compare_topics():
    topic1 = [('a', 1/3), ('b', 1/3), ('c', 1/3)]
    topic2 = [('a', 1/3), ('b', 1/3), ('c', 1/3)]
    assert ct.compare_topics(topic1, topic2) == pytest.approx(1.0)

    topic1 = [('a', 1.0)]
    topic2 = [('b', 1.0)]
    assert ct.compare_topics(topic1, topic2) == pytest.approx(0.0)

    topic1 = [('a', 1.0)]
    topic2 = [('a', 0.5), ('b', 0.5)]
    assert ct.compare_topics(topic1, topic2) == pytest.approx(sqrt(0.5))

def test_extract_similar_topics_only_perfect_matches():
    initial_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('d', 1.0)]]
    new_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('b', 1.0)], [('d', 0.5), ('e', 0.5)]]

    known_topics = ct.KnownTopics(threshold=1.0)
    known_topics.add_topics(initial_topics)
    known_topics.add_topics(new_topics)
    aggregated_topics = known_topics.topics()

    assert len(aggregated_topics) == 4
    assert sorted([len(representations) for representations in aggregated_topics]) == [1, 1, 1, 2]
    most_represented_topic = max(aggregated_topics, key=lambda x: len(x))
    print(most_represented_topic)
    assert most_represented_topic == [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('a', 1/3), ('b', 1/3), ('c', 1/3)]]

def test_extract_similar_topics_lenient_matches():
    initial_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('d', 1.0)]]
    new_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('b', 1.0)], [('d', 0.5), ('e', 0.5)]]

    known_topics = ct.KnownTopics(threshold=0.7)
    known_topics.add_topics(initial_topics)
    known_topics.add_topics(new_topics)
    aggregated_topics = known_topics.topics()

    assert len(aggregated_topics) == 3 # two topics are similar enough
    assert sorted([len(representations) for representations in aggregated_topics]) == [1, 2, 2]
    assert [[('d', 1.0)], [('d', 0.5), ('e', 0.5)]] in aggregated_topics

def test_extract_similar_topics_everything_matches():
    initial_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('d', 1.0)]]
    new_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('b', 1.0)], [('d', 0.5), ('e', 0.5)]]

    known_topics = ct.KnownTopics(threshold=0.0)
    known_topics.add_topics(initial_topics)
    known_topics.add_topics(new_topics)
    aggregated_topics = known_topics.topics()

    assert len(aggregated_topics) == min(len(initial_topics), len(new_topics))

def test_extract_similar_topics_nothing_matches():
    initial_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('d', 1.0)]]
    new_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('b', 1.0)], [('d', 0.5), ('e', 0.5)]]

    known_topics = ct.KnownTopics(threshold=1.1)
    known_topics.add_topics(initial_topics)
    known_topics.add_topics(new_topics)
    aggregated_topics = known_topics.topics()

    assert len(aggregated_topics) == len(initial_topics) + len(new_topics)
    assert sorted([representations[0] for representations in aggregated_topics]) == sorted(initial_topics + new_topics)

def test_return_values_of_add_topics():
    initial_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('d', 1.0)]]
    new_topics = [[('a', 1/3), ('b', 1/3), ('c', 1/3)], [('b', 1.0)], [('d', 0.5), ('e', 0.5)]]

    # nothing matches
    known_topics = ct.KnownTopics(threshold=1.1)
    topic_dict, matched_ids = known_topics.add_topics(initial_topics)
    assert topic_dict.keys() == set(range(len(initial_topics)))
    assert len(matched_ids) == 0

    topic_dict, matched_ids = known_topics.add_topics(new_topics)
    assert topic_dict.keys() == set(range(len(initial_topics), len(initial_topics) + len(new_topics)))
    assert len(matched_ids) == 0

    # everything matches
    known_topics = ct.KnownTopics(threshold=0.0)
    known_topics.add_topics(initial_topics)

    topic_dict, matched_ids = known_topics.add_topics(new_topics)
    assert len(topic_dict) == len(initial_topics)
    assert len(matched_ids) == len(initial_topics)

def test_average_strategy():
    topic = [('a', 1/3), ('b', 1/3), ('c', 1/3)]
    assert ct.average_strategy([topic, topic]) == topic

    topic1 = [('a', 1.0)]
    topic2 = [('a', 1/2), ('b', 1/2)]
    average = ct.average_strategy([topic1, topic2])
    assert sum([weight for _, weight in average]) == pytest.approx(1.0)
    assert average == [('a', 0.75), ('b', 0.25)]

    topic1 = [('a', 1/2), ('b', 1/2)]
    topic2 = [('a', 1/3), ('b', 1/3), ('c', 1/3)]
    average = ct.average_strategy([topic1, topic2])
    assert sum([weight for _, weight in average]) == pytest.approx(1.0)
    assert average == [('a', pytest.approx(5/12)), ('b', pytest.approx(5/12)), ('c', pytest.approx(2/12))]
