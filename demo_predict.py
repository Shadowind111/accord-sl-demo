# -*- coding: utf-8 -*-
"""Pure-python demo scoring (no pickled sklearn artifacts)."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

PKG = Path(__file__).resolve().parent
MODELS = PKG / "demo_models"

def _load(tier):
    return json.loads((MODELS / f"{tier.lower()}_logistic.json").read_text(encoding="utf-8"))

def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def _num(s):
    return pd.to_numeric(s.astype(str).str.strip().str.replace(r"^[<>]\s*", "", regex=True), errors="coerce")

def score_t1(df: pd.DataFrame) -> pd.DataFrame:
    m = _load("T1"); out = df.copy()
    z = np.full(len(out), float(m["intercept"]))
    for c, spec in m["numeric"].items():
        x = _num(out[c]) if c in out.columns else pd.Series([np.nan]*len(out))
        x = x.fillna(spec["median"])
        z += spec["coef"] * ((x - spec["mean"]) / spec["std"]).values
    for c, spec in m["categorical"].items():
        s = out[c].astype(object).where(out[c].notna(), spec["default"]).astype(str) if c in out.columns else pd.Series([spec["default"]]*len(out))
        mp = {cat: coef for cat, coef in zip(spec["categories"], spec["coefs"])}
        z += s.map(mp).fillna(0.0).values
    p = _sigmoid(z)
    return pd.DataFrame({"raw_score": p, "calibrated_score": p, "high_risk": (p >= 0.5).astype(int), "near_threshold": (np.abs(p-0.5) <= 0.05).astype(int)})

def score_t2(df: pd.DataFrame) -> pd.DataFrame:
    m = _load("T2"); out = df.copy()
    z = np.full(len(out), float(m["intercept"]))
    for c, spec in m["numeric"].items():
        x = _num(out[c]) if c in out.columns else pd.Series([np.nan]*len(out))
        x = x.fillna(spec["median"])
        z += spec["coef"] * ((x - spec["mean"]) / spec["std"]).values
    p = _sigmoid(z)
    return pd.DataFrame({"raw_score": p, "calibrated_score": p, "high_risk": (p >= 0.5).astype(int), "near_threshold": (np.abs(p-0.5) <= 0.05).astype(int)})
