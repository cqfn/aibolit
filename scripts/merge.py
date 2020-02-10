import pandas as pd

df_patterns = pd.read_csv('./target/04/04-find-patterns.csv', sep=';').set_index('filename')
df_readability = pd.read_csv('./target/05/05_readability.csv', sep=';').set_index('filename')
print(df_readability.head())

df_patterns.join(df_readability, how='inner').to_csv('./target/dataset.csv')

