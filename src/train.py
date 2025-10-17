from sklearn.datasets import load_diabetes
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib, json, os, numpy as np, random, argparse

def train(model_version: str = "v0.1", seed: int = 42, model_type: str = "lin"):
    random.seed(seed)
    np.random.seed(seed)
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"])
    y = Xy.frame["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    if model_type == "lin":
        estimator = LinearRegression()
        steps = [("scaler", StandardScaler()), ("model", estimator)]
    elif model_type == "ridge":
        estimator = Ridge(random_state=seed)
        steps = [("scaler", StandardScaler()), ("model", estimator)]
    elif model_type == "rf":
        estimator = RandomForestRegressor(n_estimators=300, random_state=seed)
        steps = [("scaler", StandardScaler()), ("model", estimator)]
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    pipe = Pipeline(steps)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", f"model-{model_version}.pkl")
    metrics_path = os.path.join("models", f"metrics-{model_version}.json")
    joblib.dump({"pipeline": pipe, "model_version": model_version, "model_type": model_type}, model_path)
    with open(metrics_path, "w") as f:
        json.dump({"rmse": rmse, "seed": seed, "model_version": model_version, "model_type": model_type}, f)


def main():
    parser = argparse.ArgumentParser(description="Train diabetes progression model")
    parser.add_argument("--version", dest="version", default="v0.1", help="model version tag, e.g., v0.1 or v0.2")
    parser.add_argument("--seed", dest="seed", type=int, default=42)
    parser.add_argument("--model", dest="model", choices=["lin", "ridge", "rf"], default="lin", help="model type: lin|ridge|rf")
    args = parser.parse_args()
    train(model_version=args.version, seed=args.seed, model_type=args.model)


if __name__ == "__main__":
    main()