from django.test import TestCase
import pandas as pd
import numpy as np
from .classification import train_models as train_classification
from .regression import train_models as train_regression

class MLEngineTestCase(TestCase):
    def setUp(self):
        # Create synthetic classification dataset (binary target)
        np.random.seed(42)
        X_class = pd.DataFrame(np.random.randn(100, 4), columns=['f1', 'f2', 'f3', 'f4'])
        y_class = pd.Series(np.random.choice([0, 1], size=100))
        self.X_class = X_class
        self.y_class = y_class

        # Create synthetic regression dataset (numeric target)
        X_reg = pd.DataFrame(np.random.randn(100, 4), columns=['f1', 'f2', 'f3', 'f4'])
        y_reg = pd.Series(np.random.randn(100) * 10)
        self.X_reg = X_reg
        self.y_reg = y_reg

    def test_classification_training(self):
        results, trained_models, best_model = train_classification(self.X_class, self.y_class)
        
        # Check that multiple results are returned (should have Logistic Regression, KNN, SVM, XGBoost, etc.)
        self.assertTrue(len(results) > 0)
        
        # Check that trained models are fully populated (crucial fix validation!)
        self.assertEqual(len(trained_models), len(results))
        self.assertIn("Logistic Regression", trained_models)
        self.assertIn("XGBoost", trained_models)
        
        # Check best model is present in results and has accuracy
        self.assertIsNotNone(best_model)
        self.assertIn("name", best_model)
        self.assertIn("accuracy", best_model)
        self.assertTrue(0.0 <= best_model["accuracy"] <= 1.0)

    def test_regression_training(self):
        results, trained_models, best_model = train_regression(self.X_reg, self.y_reg)
        
        # Check that multiple regression results are returned
        self.assertTrue(len(results) > 0)
        self.assertEqual(len(trained_models), len(results))
        self.assertIn("Linear Regression", trained_models)
        self.assertIn("XGBoost", trained_models)
        
        # Check best model regression details
        self.assertIsNotNone(best_model)
        self.assertIn("name", best_model)
        self.assertIn("accuracy", best_model) # maps to R-squared
        self.assertIn("precision", best_model) # maps to RMSE
