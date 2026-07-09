import pandas as pd


def analyze_columns(df):

    columns = []

    for column in df.columns:

        info = {

            "name": column,

            "dtype": str(df[column].dtype),

            "missing": int(
                df[column].isnull().sum()
            ),

            "unique": int(
                df[column].nunique()
            ),
        }

        if df[column].dtype == "object":

            info["most_common"] = (
                df[column]
                .mode()
                .iloc[0]
                if not df[column].mode().empty
                else "-"
            )

        else:

            info["mean"] = float(
                df[column].mean()
            ) if df[column].notnull().any() else None

            info["median"] = float(
                df[column].median()
            ) if df[column].notnull().any() else None

        columns.append(info)

    return columns


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

    "rows": len(df),

    "columns": len(df.columns),

    "column_names": df.columns.tolist(),

    "memory_usage": round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    ),

    "profile_columns": analyze_columns(df),

    "duplicate_rows": int(
        df.duplicated().sum()
    ),

    "missing_values": df.isnull().sum().to_dict(),

    "data_types": df.dtypes.astype(str).to_dict(),

    "head": df.head().to_html(
        index=False,
        classes="table table-striped"
    ),

    "describe": df.describe(
        include="all"
    ).to_html(
        classes="table table-bordered"
    ),
    }

    return profile