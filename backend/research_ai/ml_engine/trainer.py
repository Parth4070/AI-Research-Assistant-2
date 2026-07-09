from .classification import train_models as train_classification
from .regression import train_models as train_regression
from .detector import detect_problem_type

def train(df, target_column):

    problem_type, reason = detect_problem_type(
        df[target_column]
    )

    if problem_type == "classification":

        results, models = train_classification(
            df,
            target_column,
        )

    else:

        results, models = train_regression(
            df,
            target_column,
        )

    return {
        "problem_type": problem_type,
        "reason": reason,
        "results": results,
        "models": models,
    }