# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import argparse
import os
import subprocess
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(description='Filter important java files')
parser.add_argument(
    '--dir',
    help='dir for Java files search',
    required=False
)
args = parser.parse_args()


DIR_TO_CREATE = 'target/03'
dir_to_analyze = args.dir or './target/01'
current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
csv_files = []
for dir_local in Path(dir_to_analyze).iterdir():
    if dir_local.is_dir():
        print(f'Start metrics calculation for path {dir_local.parts[-1]}')
        csv_filename = f'./_tmp/{dir_local.parts[-1]}_pmd_out.csv'
        csv_files.append(csv_filename)
        f = open(csv_filename, 'w', encoding='utf-8')
        subprocess.call([
            './_tmp/pmd-bin/bin/run.sh', 'pmd',
            '-cache', './_tmp/cache',
            '-d', dir_local.absolute(), '-R', 'ruleset.xml', '-f', 'csv'
        ], stdout=f)
        print('Metrics have calculated.')
        f.close()


cur_df = pd.DataFrame(
    [['-555', 'com.google.samples',
      'Fake.java', '3', '11', 'The class AdViewIdlingResource', 'Design',
      'NcssCount']],
    columns=['Problem', 'Package', 'File', 'Priority', 'Line', 'Description', 'Rule set', 'Rule']
)
cur_df.set_index('Problem')

frames = []
for i in csv_files:
    try:
        new_frame = pd.read_csv(i)
        cur_df.set_index('Problem')
        frames.append(new_frame)
    except Exception:
        pass

print(f'we have {len(csv_files)} folders, {len(frames)} datasets')
df = pd.concat(frames)
df = df[df.Problem != -555]
df.set_index('Problem')
df.to_csv('./_tmp/pmd_out.csv')

df = pd.read_csv('./_tmp/pmd_out.csv')
df = df.drop(df.columns[[0]], axis=1)
df['class'] = 0
df.loc[df['Description'].str.contains('The class'), 'class'] = 1
rows_to_remove = df[df['class'] == 1][['File', 'class', 'Rule']]\
    .groupby(['File', 'Rule']).filter(lambda x: len(x) > 1)['File']\
    .unique().tolist()

df[df.Rule == 'CyclomaticComplexity']['Description'].str\
    .extract(r'complexity of (\d+)', expand=True)
df['cyclo'] = df['Description'].str\
    .extract(r'cyclomatic complexity of (\d+)', expand=True).astype(float)
df['ncss'] = df['Description'].str\
    .extract(r'NCSS line count of (\d+)', expand=True).astype(float)
df['npath'] = df['Description']\
    .str.extract(r'NPath complexity of (\d+)', expand=True).astype(float)

class_cyclo = df[df['class'] == 1][['File', 'cyclo']].copy().dropna()\
    .reset_index().set_index('File')
avg_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy()\
    .dropna().groupby('File').mean() \
    .reset_index() \
    .set_index('File') \
    .rename({'cyclo': 'cyclo_method_avg'}, axis='columns')

min_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'cyclo': 'cyclo_method_min'}, axis='columns')
max_method_cyclo = df[df['class'] == 0][['File', 'cyclo']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'cyclo': 'cyclo_method_max'}, axis='columns')

avg_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').mean().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_avg'}, axis='columns')
min_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_min'}, axis='columns')
max_method_npath = df[df['class'] == 0][['File', 'npath']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'npath': 'npath_method_max'}, axis='columns')

class_ncss = df[df['class'] == 1][['File', 'ncss']].copy().dropna()\
    .groupby('File').sum().reset_index().set_index('File')


avg_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').mean().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_avg'}, axis='columns')
min_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').min().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_min'}, axis='columns')
max_method_ncss = df[df['class'] == 0][['File', 'ncss']].copy().dropna()\
    .groupby('File').max().reset_index().set_index('File')\
    .rename({'ncss': 'ncss_method_max'}, axis='columns')

keys = pd.DataFrame(df.File.unique(), columns=['File']).set_index('File')
keys = keys.drop(rows_to_remove, axis=0)
metrics = keys.join(class_cyclo, how='inner')\
    .join(avg_method_cyclo, how='left')\
    .drop(columns=['index'])\
    .join(min_method_cyclo, how='left')\
    .join(max_method_cyclo, how='left')\
    .join(avg_method_npath, how='left')\
    .join(min_method_npath, how='left')\
    .join(max_method_npath, how='left')\
    .join(class_ncss, how='left')\
    .join(avg_method_ncss, how='left')\
    .join(min_method_ncss, how='left')\
    .join(max_method_ncss, how='left')\
    .reset_index()\
    .rename({'File': 'filename'}, axis='columns')\


if not os.path.isdir(DIR_TO_CREATE):
    os.makedirs(DIR_TO_CREATE)

metrics.to_csv(DIR_TO_CREATE + '/' + 'pmd_metrics.csv', sep=';', index=False)
