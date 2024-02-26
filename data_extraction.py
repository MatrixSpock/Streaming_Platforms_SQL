import os
import pandas as pd

def load_datasets():
    
    amazon_df = pd.read_csv('datasets/amazon_prime_titles.csv')
    disney_df = pd.read_csv('datasets/disney_plus_titles.csv')
    netflix_df = pd.read_csv('datasets/netflix_titles.csv')

    return amazon_df, disney_df, netflix_df
