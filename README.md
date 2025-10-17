# Virtual Diabetes Clinic Triage – ML Service

This repo contains a small ML service for a virtual diabetes clinic triage. It trains a baseline regression model on the open scikit-learn Diabetes dataset and serves predictions via an HTTP API.

## Features (v0.1)
- StandardScaler + LinearRegression with fixed seed
- RMSE reported on a held-out split and saved to `models/metrics-v0.1.json`
- FastAPI service with `/health` and `/predict`
- Docker image with baked model
- GitHub Actions CI (lint, tests, training artifact) and release workflow scaffold

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

## Train (v0.1)
```bash
python -m src.train
```
Artifacts:
- `models/model-v0.1.pkl`
- `models/metrics-v0.1.json` (example: `{ "rmse": 53.2, "seed": 42, "model_version": "v0.1" }`)

## Run API locally
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### Health
```bash
curl http://localhost:8000/health
```
Response:
```json
{"status":"ok","model_version":"v0.1"}
```

### Predict
Payload uses scikit-learn Diabetes feature names (standardized values expected):
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03,
    "s1": -0.02, "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001
  }'
```
Response:
```json
{"prediction": 152.34}
```

## Docker
```bash
docker build -t triage-ml:v0.1 .
docker run --rm -p 8000:8000 triage-ml:v0.1
```

## 发布
- 打 Tag：`git tag v0.1 && git push origin v0.1`
- GitHub Actions 将构建镜像、冒烟测试、推送到 GHCR，并创建 Release，镜像名：`ghcr.io/<org>/<repo>:v0.1`

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 2ea4819 (CI check)
### v0.2 使用
- 训练：
```bash
python -m src.train --version v0.2 --model ridge --seed 42
```
- 打包与发布：
```bash
git tag v0.2
git push origin v0.2
```
发布工作流会根据标签自动选择模型类型（v0.2 默认 ridge），并把 `models/metrics-v0.2.json` 内容附到 Release。

<<<<<<< HEAD
=======
>>>>>>> 6df35c2 (Add initial implementation of diabetes prediction service with FastAPI, Docker support, and CI/CD workflows)
=======
>>>>>>> 2ea4819 (CI check)
## CI/CD (GitHub Actions)
- PR/push: lint, tests, training smoke, artifact upload
- Tag `v*`: build image, smoke test, push to GHCR, create GitHub Release with metrics and CHANGELOG

## Versioning
See `CHANGELOG.md`.
