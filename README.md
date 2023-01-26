# Privacy Policies over Time
Juniper Lovato, Philip Mueller, Parisa Suchdev

## Data Processing

### Intermediate Datasets

These are some datasets that were generated from the original Amos et al. corpus to make analysis easier.

#### Full Corpus CSV Data

Based on: Original SQLite database

Additional processing steps:

- `poetry run python extract/extract_from_sqlite.py`
- `poetry run python extract/join.py`

#### By-Year Data

Based on: Full Corpus CSV Data

Additional processing steps:

- `python split_by_year.py data/PrivacyPolicies_df_cleaned.csv --out-prefix=data/by-year/PrivacyPolicies`

#### Negation Filtered By-Year

Based on: By-Year Data

Additional processing steps:

- `negation_filtered_policytext_PII.ipynb`

#### Negation and PII Filtered By-Year

Based on: By-Year Data

Additional processing steps:

- `negation_filtered_policytext_PII.ipynb`

### Visualizations

#### Co-Occurrence Networks

Based on: Negation and PII Filtered By-Year

Additional processing steps:

- `poetry run python generate_cooccurrence_network.py`

#### Co-Occurrence Network Backbone

Based on: Negation and PII Filtered By-Year (1997 only)

Additional processing steps:

- `poetry run python generate_cooccurrence_network.py data/filtered_pii_extracted/1997_pii_extracted.csv`
