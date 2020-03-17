import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(16, 7)
        self.fc2 = nn.Linear(7, 5)
        self.fc3 = nn.Linear(5, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class AibolitDataset(torch.utils.data.Dataset):
    def __init__(self):
        # import and initialize dataset
        df = pd.read_csv('dataset6.csv')
        df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
        df = df[(df.ncss > 20) & (df.ncss < 200) & (df.npath_method_avg < 100000.00)].copy().reset_index()
        # df = df[(df.npath_method_avg > 0.0000000000000000000000001)].copy().reset_index()
        df.rename(columns={'for_type_cast_number': 'force_type_cast_number'}, inplace=True)
        df = df[~df["filename"].str.lower().str.contains("test")]
        df.drop('filename', axis=1, inplace=True)
        df.drop('index', axis=1, inplace=True)
        columns_patterns = [
            'var_middle_number',
            # 'nested_for_number', 'nested_if_number',
            'string_concat_number', 'instance_of_number',
            'method_chain_number', 'var_decl_diff_number_11', 'var_decl_diff_number_7', 'var_decl_diff_number_5',
            'super_method_call_number', 'force_type_cast_number',
            'entropy', 'halstead volume', 'ncss_method_avg',
            'left_spaces_var', 'right_spaces_var', 'max_left_diff_spaces', 'max_right_diff_spaces'
        ]
        self.Y = df[['cyclo_method_avg']].copy().values
        new = df[columns_patterns].copy()
        self.X = pd.DataFrame(StandardScaler().fit_transform(new.values), columns=new.columns, index=new.index).values
        self._columns = new.columns

    def __getitem__(self, idx):
        # get item by index
        return torch.FloatTensor(self.X[idx]), torch.FloatTensor(self.Y[idx])

    def __len__(self):
        # returns length of data
        return len(self.X)

    @property
    def columns(self):
        """Columns property."""
        return self._columns.tolist()
