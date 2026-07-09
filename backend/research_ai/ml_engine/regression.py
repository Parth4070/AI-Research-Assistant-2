import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
)
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor

MODELS = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42),
    "SVR": SVR(),
    "XGBoost": XGBRegressor(random_state=42),
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
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, predictions)
        
        results.append({
            "name": name,
            "accuracy": float(r2), # store R2 in accuracy field of DB
            "precision": float(rmse), # map RMSE
            "f1": float(mae), # map MAE
            "recall": float(mse), # map MSE
        })
        trained_models[name] = model

    # Select the best model (highest R-squared score)
    best_model = max(
        results,
        key=(lambda x: x["accuracy"])
    )

    return results, trained_models, best_model
