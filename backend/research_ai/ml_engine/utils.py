CLASSIFICATION_MODELS = [

    "Logistic Regression",

    "Decision Tree",

    "Random Forest",

    "KNN",

    "SVM",

    "Naive Bayes",

    "XGBoost",

]

REGRESSION_MODELS = [

    "Linear Regression",

    "Decision Tree",

    "Random Forest",

    "SVR",

    "XGBoost",

]

def get_recommended_models(problem_type):

    if problem_type == "classification":

        return CLASSIFICATION_MODELS

    return REGRESSION_MODELS