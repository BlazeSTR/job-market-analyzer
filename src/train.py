import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from config import PROCESSED_PATH


def prepare_data(df: pd.DataFrame):
    valid_salaries = df[df["salary_min"] > 0].copy()

    if len(valid_salaries) < 5:
        raise ValueError("Not enough salary data to train a model. Fetch more listings!")

    skill_dummies = valid_salaries["skills"].fillna("").str.get_dummies(sep=",")
    skill_dummies = skill_dummies.add_prefix("skill_")
    valid_salaries = pd.concat([valid_salaries, skill_dummies], axis=1)
    skill_cols = sorted(skill_dummies.columns)  # sorted = reproducible ordering

    feature_cols = skill_cols + ["skill_count"]

    X = valid_salaries[feature_cols]
    y = valid_salaries["salary_min"]

    return X, y, feature_cols


def main():
    if not PROCESSED_PATH.exists():
        print("Error: Processed CSV not found. Run clean.py first.")
        return

    df = pd.read_csv(PROCESSED_PATH)
    print(f"Loaded {len(df)} total job records.")

    try:
        X, y, feature_names = prepare_data(df)
    except ValueError as e:
        print(f"Data error: {e}")
        return

    print(f"Filtered down to {len(X)} jobs with valid salary listings.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n--- Model Performance ---")
    print(f"Mean Absolute Error: ${mae:,.2f}")
    print(f"R^2 Score: {r2:.2f}")

    importances = pd.Series(model.feature_importances_, index=feature_names)
    print("\nTop Predictors for Higher Salary:")
    print(importances.sort_values(ascending=False).head(5))


if __name__ == "__main__":
    main()
