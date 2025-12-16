
# ----------------------------
# FastAPI app
# ----------------------------

import os
import pickle
import json
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi import Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.preprocess import to_dataframe, engineer_features, scale
from app.player import RookieStats

app = FastAPI(
    title="NBA Longevity Scoring API",
    description="Prédit si un rookie NBA durera ≥ 5 ans (TARGET_5Yrs).",
    version="1.0.0"
)

import os
from pathlib import Path

# Get the directory of the current script
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "nba_final_model.pkl"
FEATURE_LIST_PATH = BASE_DIR / "feature_names.json"
SCALER_PATH = BASE_DIR / "scaler.pkl"

with open(MODEL_PATH, "rb") as f:
    MODEL = pickle.load(f)

with open(FEATURE_LIST_PATH, "r") as f:
    FEATURE_LIST: List[str] = json.load(f)


with open(SCALER_PATH, "rb") as f:
    SCALER_BUNDLE = pickle.load(f) 

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_path": str(MODEL_PATH),
        "feature_list_path": str(FEATURE_LIST_PATH),
        "scaler_loaded": str(SCALER_PATH),
        "n_features_expected": len(FEATURE_LIST),
    }
@app.get("/metadata")
def metadata():
    return {
        "model_type": type(getattr(MODEL, "named_steps", {}).get("clf", MODEL)).__name__,
        "features_expected": FEATURE_LIST,
    }


# @app.get("/debug")
# def debug():
#     return {
#         "model_path": str(MODEL_PATH),
#         "n_features_expected": len(FEATURE_LIST),
#         "first_10_expected": FEATURE_LIST[:10],
#         "scaler_loaded": str(SCALER_PATH),
#         "scaled_columns": SCALER_BUNDLE["feature_names"]
#     }


class PredictResponse(BaseModel):
    prediction: int = Field(..., description="0=non durable, 1=durable")
    probability: float = Field(..., ge=0, le=1)
    threshold: float = Field(..., ge=0, le=1)
    model: str = Field(..., description="Model file used for prediction")

example_payload = {
  "gp": 65, "min": 24.3, "pts": 11.2, "fgm": 4.3, "fga": 9.7, "fg_pct": 44.5,
  "three_p_made": 1.6, "three_p_attempts": 4.5, "three_p_pct": 35.5,
  "ftm": 1.1, "fta": 1.3, "ft_pct": 82,
  "oreb": 0.8, "dreb": 3.1, "reb": 3.9,
  "ast": 2.4, "stl": 0.9, "blk": 0.3, "tov": 1.7
}

@app.post("/predict",
    response_model=PredictResponse,
    tags=["Scoring"],
    summary="Prédire la durabilité (≥5 ans)",
    description="Calcule la probabilité que le joueur soit durable à partir des stats rookies.")
def predict(payload: RookieStats = Body(
        example=example_payload  
    ), threshold: float = Query(0.5, ge=0.0, le=1.0)):


    try:
        df_raw = to_dataframe(payload)
        df_eng = engineer_features(df_raw)
        X = scale(df_eng, FEATURE_LIST, SCALER_BUNDLE)
       
        proba = float(MODEL.predict_proba(X)[:, 1][0])
    
        pred = int(proba >= threshold)

        return PredictResponse(
            prediction=pred,
            probability=proba,
            threshold=threshold,
            model=str(MODEL_PATH.name),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {e}")
    

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"error": type(exc).__name__, "message": str(exc)}
    )