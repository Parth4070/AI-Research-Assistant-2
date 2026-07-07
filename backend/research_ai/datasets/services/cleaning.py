import pandas as pd

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

        if df[column].dtype == "object":

            modes = df[column].mode()
            value = modes[0] if not modes.empty else ""

        else:

            value = df[column].mean()

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