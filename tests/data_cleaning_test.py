import pandas as pd

from lib import data_cleaning

def test_tokenize_series():
    series = pd.Series([
        "Hello world - this is it. i is a good variable.",
        "Good-bye, world!",
        "Good muffins cost $3.88\nin New York.\n\nThanks."
    ])
    result = data_cleaning.tokenize_series(series)
    assert result[0] == ["Hello", "world", "this", "is", "it", "i", "is", "a", "good", "variable"]
    assert result[1] == ["Good", "bye", "world"]
    assert result[2] == ["Good", "muffins", "cost", "3", "88", "in", "New", "York", "Thanks"]

def test_remove_non_letter_words():
    series = pd.Series([["hello", "world", "1", "2", "3"], ["òffice", "후원업체", "123", "atlético"]])
    result = data_cleaning.remove_non_letter_words(series)
    assert result[0] == ["hello", "world"]
    assert result[1] == []

def test_remove_stopwords():
    series = pd.Series([
        ["Hello", "world", "this", "is", "it", "i", "is", "a", "good", "variable"], ["world", "world"]
    ])
    result = data_cleaning.remove_stopwords(series)
    assert sorted(result[0]) == sorted(["Hello", "world", "good", "variable"])
    # preserves duplicates
    assert sorted(result[1]) == sorted(["world", "world"])

def test_stem_series():
    series = pd.Series([["Swimming", "catlike", "good", "variable"], ["Goodbye", "arguably"]])
    result = data_cleaning.stem_series(series, parallel=True)
    assert result[0] == ["swim", "catlik", "good", "variabl"]
    assert result[1] == ["goodby", "arguabl"]
    result = data_cleaning.stem_series(series, parallel=False)
    assert result[0] == ["swim", "catlik", "good", "variabl"]
    assert result[1] == ["goodby", "arguabl"]

def test_combine_lists_of_bags():
    bag1 = pd.DataFrame([[1, 2], [4, 5]], columns=["a", "b"])
    bag2 = pd.DataFrame([[7, 8], [10, 11]], columns=["a", "c"])
    result = data_cleaning.combine_lists_of_bags(bag1, bag2)

    assert result["a"][0] == 1
    assert result["a"][1] == 4
    assert result["a"][2] == 7
    assert result["a"][3] == 10

    assert result["b"][0] == 2
    assert result["b"][1] == 5
    assert result["b"][2] == 0
    assert result["b"][3] == 0

    assert result["c"][0] == 0
    assert result["c"][1] == 0
    assert result["c"][2] == 8
    assert result["c"][3] == 11

    assert result["a"][0].dtype == "uint16"

# integration test
def test_clean_series():
    series = pd.Series(["Hello world - this is 9. i is a good variable.", "The Good-bye to the world."])
    result = data_cleaning.clean_series(series)
    assert result[0] == ["hello", "world", "good", "variabl"]
    assert result[1] == ["good", "bye", "world"]
