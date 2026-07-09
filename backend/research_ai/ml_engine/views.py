from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MLExpriment
from datasets.models import Dataset
import pandas as pd
import pickle
from django.core.files.base import ContentFile
from .forms import TrainModelForm
from .classification import train_models as train_classification_models
from .regression import train_models as train_regression_models

# Create your views here.
@login_required
def train_model_view(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, project__owner=request.user)
    file_path = dataset.file.path

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")

    # Get non-empty columns
    columns = [col for col in df.columns if df[col].notnull().any()]

    if not columns:
        messages.error(request, "The dataset has no valid columns with data.")
        return redirect("dataset_detail", dataset.id)

    default_target = columns[-1] if columns else ""

    if request.method == "POST":
        form = TrainModelForm(request.POST, columns=columns)
        if form.is_valid():
            target_column = form.cleaned_data['target_column']
            problem_type = form.cleaned_data['problem_type']

            # Clean and prepare the training data
            train_df = df.dropna(subset=[target_column]).copy()
            y = train_df[target_column]
            X = train_df.drop(columns=[target_column])

            # Simple imputation for training features to prevent sklearn crash
            for col in X.columns:
                if X[col].isnull().any():
                    if X[col].dtype in ['int64', 'float64']:
                        X[col] = X[col].fillna(X[col].mean())
                    else:
                        mode_val = X[col].mode()
                        X[col] = X[col].fillna(mode_val[0] if not mode_val.empty else "Missing")

            # Encode categorical features
            X = pd.get_dummies(X, drop_first=True)

            try:
                if problem_type == "classification":
                    results, trained_models, best_model_details = train_classification_models(X, y)
                else:
                    results, trained_models, best_model_details = train_regression_models(X, y)

                best_model_name = best_model_details["name"]
                best_model_instance = trained_models[best_model_name]

                # Serialize the best model and save it
                model_bytes = pickle.dumps(best_model_instance)
                model_filename = f"model_{dataset.id}_{best_model_name.replace(' ', '_').lower()}.pkl"
                model_file = ContentFile(model_bytes, name=model_filename)

                # Save experiment details
                experiment = MLExpriment.objects.create(
                    dataset=dataset,
                    target_column=target_column,
                    problem_type=problem_type,
                    best_model=best_model_name,
                    accuracy=best_model_details.get("accuracy"),
                    precision=best_model_details.get("precision"),
                    f1_score=best_model_details.get("f1"),
                    recall=best_model_details.get("recall"),
                    model_file=model_file
                )

                context = {
                    "dataset": dataset,
                    "form": form,
                    "results": results,
                    "best_model": best_model_details,
                    "experiment": experiment,
                    "success": True
                }
                return render(request, "ml_engine/train.html", context)

            except Exception as e:
                messages.error(request, f"Error during model training: {str(e)}")
    else:
        # Pre-detect the target column's problem type
        try:
            target_series = df[default_target]
            if target_series.dtype == "object" or target_series.nunique() <= 10:
                detected_type = "classification"
            else:
                detected_type = "regression"
        except Exception:
            detected_type = "classification"

        form = TrainModelForm(columns=columns, initial={
            "target_column": default_target,
            "problem_type": detected_type
        })

    return render(request, "ml_engine/train.html", {"dataset": dataset, "form": form})