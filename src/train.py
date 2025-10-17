from sklearn.datasets import load_diabetes
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib, json, os, numpy as np, random

def train(model_version: str = "v0.1", seed: int = 8):
    random.seed(seed)
    np.random.seed(seed)
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"])
    y = Xy.frame["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    pipe = Pipeline([("scaler", StandardScaler()), ("lr", LinearRegression())])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", f"model-{model_version}.pkl")
    metrics_path = os.path.join("models", f"metrics-{model_version}.json")
    joblib.dump({"pipeline": pipe, "model_version": model_version}, model_path)
    with open(metrics_path, "w") as f:
        json.dump({"rmse": rmse, "seed": seed, "model_version": model_version}, f)
if __name__ == "__main__":
    train()