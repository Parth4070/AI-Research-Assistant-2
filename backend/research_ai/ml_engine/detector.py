import pandas as pd


def detect_problem_type(target):

    if target.dtype == "object":

        return (
            "classification",
            "Target column is categorical."
        )

    if target.nunique() <= 10:

        return (
            "classification",
            f"Target has only {target.nunique()} unique values."
        )

    return (
        "regression",
        f"Target has {target.nunique()} unique numeric values."
    )