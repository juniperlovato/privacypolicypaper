# Privacy Policies over Time
Juniper Lovato, Philip Mueller, Parisa Suchdev

## Data Processing

### Intermediate Datasets

These are some datasets that were generated from the original Amos et al. corpus to make ananalysis easier.

#### Full Corpus CSV Data

Based on: Original SQLite database
Additional processing steps:
- `extract/extract_from_sqlite.py`
- `extract/join.py`

#### By-Year Data

Based on: Full Corpus CSV Data
Additional processing steps:
- `split_by_year.py data/PrivacyPolicies_df_cleaned.csv --out-prefix=data/by-year/PrivacyPolicies`

#### Negation Filtered By-Year

Based on: By-Year Data
Additional processing steps:
- `negation_filtered_policytext_PII.ipynb`

#### PII Filtered By-Year

Based on: Negation Filtered By-Year
Additional processing steps: 
- `negation_filtered_policytext_PII.ipynb`
