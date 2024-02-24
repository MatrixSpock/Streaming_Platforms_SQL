# data_extraction.py
import pandas as pd
import yaml

def load_datasets(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    db_config = config['database_config']
    dataset1_path = config['dataset_paths']['dataset1']
    dataset2_path = config['dataset_paths']['dataset2']
    dataset3_path = config['dataset_paths']['dataset3']

    amazon_df = pd.read_csv(dataset1_path)
    disney_df = pd.read_csv(dataset2_path)
    netflix_df = pd.read_csv(dataset3_path)

    return amazon_df, disney_df, netflix_df
