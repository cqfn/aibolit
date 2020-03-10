import pandas as pd

df_pmd_metrics = pd.read_csv('./target/03/pmd_metrics.csv', sep=';').set_index('filename')
df_patterns = pd.read_csv('./target/04/04-find-patterns.csv', sep=';').set_index('filename')
df_readability = pd.read_csv('./target/05/05_readability.csv', sep=';').set_index('filename')
df_halstead = pd.read_csv('./target/06/06_halstead_volume.csv', sep=';').set_index('filename')

first_df = df_pmd_metrics.join(df_readability, how='inner')
patterns_read_df = df_patterns.join(first_df, how='inner')
halstead = patterns_read_df.join(df_halstead, how='inner')
print(halstead.head())
halstead.to_csv('./target/dataset.csv')
