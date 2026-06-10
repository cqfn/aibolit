# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import argparse
import os
import subprocess
from pathlib import Path

import pandas as pd

DIR_TO_CREATE = 'target/03'


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Filter important java files')
    parser.add_argument(
        '--dir',
        help='dir for Java files search',
        required=False
    )
    return parser


def collect_analysis_targets(dir_to_analyze: Path) -> list[Path]:
    return [
        path for path in sorted(dir_to_analyze.iterdir(), key=lambda path: path.name)
        if path.is_dir() or path.suffix == '.java'
    ]


def csv_filename_for_path(path: Path) -> str:
    if path.is_dir():
        return f'./_tmp/{path.name}_pmd_out.csv'
    return f'./_tmp/file_{path.stem}_pmd_out.csv'


def run_pmd(dir_to_analyze: Path) -> list[str]:
    csv_files = []
    for path_to_analyze in collect_analysis_targets(dir_to_analyze):
        print(f'Start metrics calculation for path {path_to_analyze.name}')
        csv_filename = csv_filename_for_path(path_to_analyze)
        csv_files.append(csv_filename)
        with open(csv_filename, 'w', encoding='utf-8') as file_descriptor:
            subprocess.call([
                './_tmp/pmd-bin/bin/run.sh', 'pmd',
                '-cache', './_tmp/cache',
                '-d', path_to_analyze.absolute(), '-R', 'ruleset.xml', '-f', 'csv'
            ], stdout=file_descriptor)
        print('Metrics have calculated.')
    return csv_files


def read_pmd_frames(csv_files: list[str]) -> list[pd.DataFrame]:
    cur_df = pd.DataFrame(
        [['-555', 'com.google.samples',
          'Fake.java', '3', '11', 'The class AdViewIdlingResource', 'Design',
          'NcssCount']],
        columns=[
            'Problem', 'Package', 'File', 'Priority', 'Line', 'Description',
            'Rule set', 'Rule'
        ]
    )
    cur_df.set_index('Problem')

    frames = []
    for csv_file in csv_files:
        try:
            new_frame = pd.read_csv(csv_file)
            cur_df.set_index('Problem')
            frames.append(new_frame)
        except Exception:
            pass
    return frames


def build_metrics(frames: list[pd.DataFrame]) -> pd.DataFrame:
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
    return keys.join(class_cyclo, how='inner')\
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
        .rename({'File': 'filename'}, axis='columns')


def main() -> None:
    args = create_parser().parse_args()
    dir_to_analyze = Path(args.dir or './target/01')
    csv_files = run_pmd(dir_to_analyze)
    frames = read_pmd_frames(csv_files)
    print(f'we have {len(csv_files)} analysis targets, {len(frames)} datasets')
    metrics = build_metrics(frames)

    if not os.path.isdir(DIR_TO_CREATE):
        os.makedirs(DIR_TO_CREATE)

    metrics.to_csv(DIR_TO_CREATE + '/' + 'pmd_metrics.csv', sep=';', index=False)


if __name__ == '__main__':
    main()
