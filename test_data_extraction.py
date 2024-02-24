# test_data_extraction.py
from data_extraction import load_datasets

def test_data_extraction():
    amazon_df, disney_df, netflix_df = load_datasets()

    # Check that the data frames are not empty
    assert not amazon_df.empty, "Amazon data frame is empty"
    assert not disney_df.empty, "Disney data frame is empty"
    assert not netflix_df.empty, "Netflix data frame is empty"

    # Check for expected number of columns or any other data integrity checks
    assert len(amazon_df.columns) >= 5, "Amazon data frame has too few columns"
    assert len(disney_df.columns) >= 5, "Disney data frame has too few columns"
    assert len(netflix_df.columns) >= 5, "Netflix data frame has too few columns"

    # Optionally, check the number of rows if you expect a minimum amount of data
    # assert len(amazon_df) > 100, "Amazon data frame has too few rows"
