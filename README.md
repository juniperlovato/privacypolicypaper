# Privacy Policies over Time
Juniper Lovato, Philip Mueller, Parisa Suchdev, Peter Dodds

## Data Processing

### Intermediate Datasets

These are some datasets that were generated from the original Amos et al. corpus to make analysis easier.

#### Full Corpus CSV Data

Based on: Original SQLite database

Additional processing steps:

- `extract/extract_from_sqlite.py`
- `extract/join.py`

#### By-Year Data

Based on: Full Corpus CSV Data

Additional processing steps:

- `split_by_year.py`

#### Negation Filtered By-Year Data

Based on: By-Year Data

Additional processing steps:

- `negation_filtered_policytext_PII.ipynb`

#### Negation and PII Filtered By-Year Data

Based on: By-Year Data

Additional processing steps:

- `negation_filtered_policytext_PII.ipynb`

#### Co-Occurrence Networks

Based on: Negation and PII Filtered By-Year

Additional processing steps:

- `generate_cooccurrence_network.py`

#### Co-Occurrence Network Backbone

Based on: Negation and PII Filtered By-Year (1997 only)

Additional processing steps:

- `generate_cooccurrence_network.py`

#### SBM Topic Model Topics 

Based on: Negation and PII Filtered By-Year Data

Additional processing steps:

- `SBM_topic-Model_Privacy_Policy_Paper_2023.ipynb`

#### SBM Topic Model Minimum Description Length 

Based on: By-Year Data

Additional processing steps:

- `SBM_topic-Model_Privacy_Policy_Paper_2023.ipynb`
- `countwords_uniquewords_Privacy_Policy_Paper_2023.ipynb`

### Visualizations

#### Frequency Distribution of PII Data Types

Based on: Negation and PII Filtered By-Year 

Additional processing steps:

- `Viz_PII_Frequency_Privacy_Policy_Paper_2023.ipynb`
