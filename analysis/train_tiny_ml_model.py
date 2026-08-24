from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import (
    KFold,
    cross_val_predict
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# --------------------------------------------------
# 1. Define folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "ml_feature_dataset.csv"
)

FIGURE_FILE = (
    PROJECT_ROOT
    / "figures"
    / "ml_parity_plot.png"
)

PREDICTION_FILE = (
    PROJECT_ROOT
    / "data"
    / "ml_predictions.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "data"
    / "tiny_random_forest_model.joblib"
)


# --------------------------------------------------
# 2. Read dataset
# --------------------------------------------------

data = pd.read_csv(
    DATA_FILE
)


# --------------------------------------------------
# 3. Define ML input features
# --------------------------------------------------

feature_columns = [

    "Al_fraction",

    "Al_Al_pair_fraction",

    "Al_Co_pair_fraction",

    "Co_Co_pair_fraction"
]


X = data[
    feature_columns
]


y = data[
    "formation_energy_eV_per_atom"
]


# --------------------------------------------------
# 4. Create Random Forest model
# --------------------------------------------------

model = RandomForestRegressor(

    n_estimators=200,

    max_depth=4,

    random_state=42
)


# --------------------------------------------------
# 5. Five-fold cross-validation
# --------------------------------------------------

cv = KFold(

    n_splits=5,

    shuffle=True,

    random_state=42
)


predictions = cross_val_predict(

    model,

    X,

    y,

    cv=cv
)


# --------------------------------------------------
# 6. Calculate evaluation metrics
# --------------------------------------------------

mae = mean_absolute_error(
    y,
    predictions
)


mse = mean_squared_error(
    y,
    predictions
)


rmse = np.sqrt(
    mse
)


r2 = r2_score(
    y,
    predictions
)


print()
print("----------------------------------------")
print("TINY ML MODEL RESULTS")
print("----------------------------------------")

print(
    f"MAE  = {mae:.6f} eV/atom"
)

print(
    f"RMSE = {rmse:.6f} eV/atom"
)

print(
    f"R2   = {r2:.6f}"
)

print("----------------------------------------")


# --------------------------------------------------
# 7. Save predictions
# --------------------------------------------------

prediction_data = data.copy()

prediction_data[
    "ML_predicted_formation_energy_eV_per_atom"
] = predictions


prediction_data.to_csv(
    PREDICTION_FILE,
    index=False
)


# --------------------------------------------------
# 8. Fit final model using all 21 structures
# --------------------------------------------------

model.fit(
    X,
    y
)


joblib.dump(
    model,
    MODEL_FILE
)


# --------------------------------------------------
# 9. Report feature importance
# --------------------------------------------------

print()
print("Feature importance:")
print()


for feature, importance in zip(
    feature_columns,
    model.feature_importances_
):

    print(
        f"{feature}: "
        f"{importance:.4f}"
    )


# --------------------------------------------------
# 10. Create parity plot
# --------------------------------------------------

plt.figure(
    figsize=(7, 7)
)


plt.scatter(
    y,
    predictions,
    s=70
)


minimum = min(
    y.min(),
    predictions.min()
)


maximum = max(
    y.max(),
    predictions.max()
)


plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)


plt.xlabel(
    "CHGNet-derived formation energy (eV/atom)"
)

plt.ylabel(
    "Random Forest predicted energy (eV/atom)"
)

plt.title(
    "Tiny ML surrogate: predicted vs target energy"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()


plt.savefig(
    FIGURE_FILE,
    dpi=300
)


print()
print(
    "Parity plot saved as:"
)

print(
    FIGURE_FILE
)

print()

print(
    "Predictions saved as:"
)

print(
    PREDICTION_FILE
)

print()

print(
    "Final trained model saved as:"
)

print(
    MODEL_FILE
)


plt.show()