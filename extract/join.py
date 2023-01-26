# read dumped tables, join them, drop a few superfluous columns, and write to csv

import os

import pandas as pd

script_dir = os.path.dirname(__file__)

policy_snapshots = pd.read_csv(os.path.join(script_dir, '../data/policy_snapshots.csv.xz'))
policy_texts = pd.read_csv(os.path.join(script_dir, '../data/cleaned/policy_texts_cleaned.csv.xz'))
sites = pd.read_csv(os.path.join(script_dir, '../data/sites.csv'))
alexa_ranks = pd.read_csv(os.path.join(script_dir, '../data/alexa_ranks.csv'))

# This is strange - why would we merge in pandas, instead of letting SQLite do the work?
joined_df = policy_snapshots

# Left join with policy text table
joined_df = pd.merge(joined_df, policy_texts, how="left", left_on="policy_text_id", right_on="id")

# Left join with sites table
joined_df = pd.merge(joined_df, sites, how="left", left_on="site_id", right_on="id")

# Left join with alexa ranks table
joined_df = pd.merge(joined_df, alexa_ranks, how="left", on=['site_id', 'year', 'phase'])

# export the joined table to csv
# joined_df.to_csv(os.path.join(script_dir, '../data/JoinedComboData.corrected.csv'), index=False)

# remove all columns except the ones we need and dump to csv
needed_columns = [
    'site_id', 'policy_url', 'year', 'policy_text_id', 'policy_title', 'policy_text', 'length', 'simhash', 'domain', 'categories', 'rank'
]
joined_df = joined_df[needed_columns]
joined_df.to_csv(os.path.join(script_dir, '../data/PrivacyPolicies_df_cleaned.csv'), index=False)
