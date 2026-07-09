import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier

MODELS = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(random_state=42),

    "KNN":
        KNeighborsClassifier(),

    "SVM":
        SVC(),

    "Naive Bayes":
        GaussianNB(),

    "XGBoost":
        XGBClassifier(
            eval_metric="logloss",
            random_state=42,
        ),
}

def train_models(X, y):

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    results = []

    trained_models = {}

    for name, model in MODELS.items():

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_test,
        )

        results.append({

            "name": name,

            "accuracy":
                accuracy_score(
                    y_test,
                    predictions,
                ),

            "precision":
                precision_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                ),

            "recall":
                recall_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                ),

            "f1":
                f1_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0,
                ),
        })

        trained_models[name] = model

    best_model = max(
        results,
        key=(lambda x: x["accuracy"])
    )

    return results, trained_models, best_model