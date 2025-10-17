<<<<<<< HEAD
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import os, joblib


MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join("models", f"model-{MODEL_VERSION}.pkl"))


class Features(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    obj = joblib.load(path)
    return obj["pipeline"], obj.get("model_version", MODEL_VERSION)


app = FastAPI(title="Diabetes Progression Service", version=MODEL_VERSION)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"error": "validation_error", "details": exc.errors()})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_error", "message": str(exc)})


try:
    PIPELINE, LOADED_VERSION = load_model(MODEL_PATH)
except FileNotFoundError:
    PIPELINE, LOADED_VERSION = None, MODEL_VERSION


@app.get("/health")
async def health():
    status = "ok" if PIPELINE is not None else "model_missing"
    return {"status": status, "model_version": LOADED_VERSION}


@app.post("/predict")
async def predict(payload: Features):
    if PIPELINE is None:
        raise HTTPException(status_code=503, detail={"error": "model_unavailable", "message": "Model not loaded"})
    data = [[
        payload.age, payload.sex, payload.bmi, payload.bp, payload.s1,
        payload.s2, payload.s3, payload.s4, payload.s5, payload.s6
    ]]
    pred = float(PIPELINE.predict(data)[0])
    return {"prediction": pred}



=======
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import os, joblib


MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join("models", f"model-{MODEL_VERSION}.pkl"))


class Features(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    obj = joblib.load(path)
    return obj["pipeline"], obj.get("model_version", MODEL_VERSION)


app = FastAPI(title="Diabetes Progression Service", version=MODEL_VERSION)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"error": "validation_error", "details": exc.errors()})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_error", "message": str(exc)})


try:
    PIPELINE, LOADED_VERSION = load_model(MODEL_PATH)
except FileNotFoundError:
    PIPELINE, LOADED_VERSION = None, MODEL_VERSION


@app.get("/health")
async def health():
    status = "ok" if PIPELINE is not None else "model_missing"
    return {"status": status, "model_version": LOADED_VERSION}


@app.post("/predict")
async def predict(payload: Features):
    if PIPELINE is None:
        raise HTTPException(status_code=503, detail={"error": "model_unavailable", "message": "Model not loaded"})
    data = [[
        payload.age, payload.sex, payload.bmi, payload.bp, payload.s1,
        payload.s2, payload.s3, payload.s4, payload.s5, payload.s6
    ]]
    pred = float(PIPELINE.predict(data)[0])
    return {"prediction": pred}


<<<<<<< HEAD
>>>>>>> 6df35c2 (Add initial implementation of diabetes prediction service with FastAPI, Docker support, and CI/CD workflows)
=======

>>>>>>> 2ea4819 (CI check)
