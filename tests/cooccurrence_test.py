from lib import cooccurrence
import pandas as pd

def test_build_matrix():
    documents = [
        "nokia taken appropriate measures prevent unauthorized personal information inaccuracy biometric geolocation",
        "biometric geolocation ip address biometric",
        "dog cat bird food water shelter address information",
    ]
    vocabulary = [
        "personal information",
        "biometric",
        "geolocation",
        "ip address",
    ]
    matrix = cooccurrence.build_matrix(documents, vocabulary)

    print(matrix)

    assert matrix.shape == (len(vocabulary), len(vocabulary))
    assert (matrix == matrix.T).all().all()
    assert matrix.loc['biometric', 'geolocation'] == 2
    assert matrix.loc['biometric', 'ip address'] == 1
    assert matrix.loc['biometric', 'personal information'] == 1
    assert matrix.loc['geolocation', 'ip address'] == 1
    assert matrix.loc['geolocation', 'personal information'] == 1
    assert matrix.loc['ip address', 'personal information'] == 0
    assert matrix.loc['personal information', 'personal information'] == 0
