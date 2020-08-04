from aibolit.model.model import PatternRankingModel
from pathlib import Path

if __name__ == '__main__':
    m = PatternRankingModel()
    files = [str(x.absolute()) for x in Path(r'D:\target\0001\fast').glob('*.java')]
    print(f'Training {files}')
    patterns = ['P12', 'P31', 'M2']
    dataset = m.train_model(files, patterns, 'M2')
    print(dataset.head())
    patterns = ['P12', 'P88', 'M2']  # feature p88 doesn't exist in config
    dataset = m.train_model(files, patterns, 'M2')
    print(dataset.head())
