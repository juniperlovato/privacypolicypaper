# Sanity checks for the list of PII terms

from lib import pii_terms

# There should not be duplicate terms for a given data type.
def test_no_duplicates():
    terms = pii_terms.get_list()

    if len(set(terms)) != len(terms):
        print(f"{len(terms)} terms")
        print("Duplicate terms:")
        print(set([term for term in terms if terms.count(term) > 1]))
        assert False
    else:
        assert True

# cleaned terms should be all lower case
def test_cleaned_terms():
    terms = pii_terms.get_list(cleaning_steps=set(['downcase']))
    for term in terms:
        assert term == term.lower()
