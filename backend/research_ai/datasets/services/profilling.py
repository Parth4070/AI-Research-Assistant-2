import pandas as pd


def profile_dataset(file_path):
    """
    Reads a dataset and returns useful information.
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format.")

    profile = {
        "dataframe": df,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "head": df.head().to_html(
            classes="table",
            index=False
        ),
        "describe": df.describe(include="all"),
    }

    return profile