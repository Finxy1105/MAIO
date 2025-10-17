import os, json
from src.train import train


def test_train_creates_artifacts(tmp_path):
    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        os.makedirs("models", exist_ok=True)
        train(model_version="v0.1-test", seed=42)
        assert os.path.exists("models/model-v0.1-test.pkl")
        assert os.path.exists("models/metrics-v0.1-test.json")
        with open("models/metrics-v0.1-test.json") as f:
            metrics = json.load(f)
        assert "rmse" in metrics and metrics["model_version"] == "v0.1-test"
    finally:
        os.chdir(cwd)


