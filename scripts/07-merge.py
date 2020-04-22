import pandas as pd

df_pmd_metrics = pd.read_csv('./target/03/pmd_metrics.csv', sep=';').set_index('filename')
df_patterns = pd.read_csv('./target/04/04-find-patterns.csv', sep=';').set_index('filename')
df_halstead = pd.read_csv('./target/06/06_halstead_volume.csv', sep=';').set_index('filename')

first_df = df_pmd_metrics.join(df_patterns, how='inner')
halstead = first_df.join(df_halstead, how='inner')
print(halstead.head())
halstead.to_csv('./target/dataset.csv')
