import pandas as pd
from pandas.api.types import is_numeric_dtype, is_bool_dtype

def remove_duplicates(df):
    """
    Removes duplicate values.
    """

    before = len(df)
    df = df.drop_duplicates().copy()
    after = len(df)

    return df, (before - after)

def impute_values(df):
    """
    Fills missing values.

    Numberical -> Mean
    Categorical -> Mode
    """

    filled = {}
    for column in df.columns:

        if is_numeric_dtype(df[column]) and not is_bool_dtype(df[column]):

            value = df[column].mean()

        else:

            modes = df[column].mode()
            value = modes[0] if not modes.empty else ""

        missing = df[column].isnull().sum()

        if missing > 0:

            df[column] = df[column].fillna(value)

            filled[column] = int(missing)

    return df, filled

def clean_dataset(df):
    report = {}

    df, duplicates = remove_duplicates(df)
    report["duplicates_removed"] = duplicates
    df, missing = impute_values(df)
    report["missing_filled"] = missing
    return df, report