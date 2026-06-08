# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os

import pandas as pd

current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
target_folder = os.getenv('TARGET_FOLDER')
if target_folder:
    os.chdir(target_folder)

df_patterns = pd.read_csv('./target/04/04-find-patterns.csv', sep=';')
df_patterns.set_index(['filepath', 'class_name', 'component_index']).to_csv('./target/dataset.csv')
