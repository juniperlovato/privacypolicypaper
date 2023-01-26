import argparse

import pandas as pd

from lib import splitting

# Split data in a pandas dataframe by year.
# We assume there to be a column named "year" in the dataframe.

argparser = argparse.ArgumentParser()
argparser.add_argument("input", help="input file path")
argparser.add_argument("--out-prefix", help="output file path prefix")

args = argparser.parse_args()

df = pd.read_csv(args.input)

# Split the dataframe by year
df_by_year = splitting.split_by_column(df, "year", unique_by="site_id")

# Write each year's dataframe to a separate file
for year, df in df_by_year.items():
    df.to_csv(args.out_prefix + "-" + str(year) + ".csv", index=False)
