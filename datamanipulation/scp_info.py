import pandas as pd

def add_scp_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """Add to the dataframe a column representing in which other scp was the scp found

    Args:
        df (pd.DataFrame): data frame that contains all the information extracted from the webpage

    Returns:
        pd.DataFrame: the same data frame but with a column that contains an array of scps which indicates that is has been interacting with that other scp
    """
    pass

