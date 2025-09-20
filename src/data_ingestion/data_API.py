#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# src/data_ingestion/data_API.py

import os
import time
import random
import pytz
import shutil
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional

import requests
from requests.exceptions import HTTPError
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

# ==========================
# Configuración básica
# ==========================
TZ = pytz.timezone("America/Bogota")
DATA_DIR = Path(os.getenv("DATA_DIR", "data/raw"))
STATE_DIR = Path(os.getenv("STATE_DIR", "data/state"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = 'GuajiraWindForecast/1.0 (Academic Research)'

MUNICIPIOS: Dict[str, tuple] = {
    "riohacha": (11.5447, -72.9072),
    "maicao": (11.3776, -72.2391),
    "uribia": (11.7147, -72.2652),
    "manaure": (11.7794, -72.4469),
    "fonseca": (10.8306, -72.8517),
    "san_juan_del_cesar": (10.7695, -73.0030),
    "albania": (11.1608, -72.5922),
    "barrancas": (10.9577, -72.7947),
    "distraccion": (10.8958, -72.8869),
    "el_molino": (10.6528, -72.9247),
    "hatonuevo": (11.0694, -72.7647),
    "la_jagua_del_pilar": (10.5108, -73.0714),
    "mingueo": (11.2000, -73.3667),
}

HOUR_FIELDS_ALL = "wind_speed_10m,wind_direction_10m,temperature_2m,relative_humidity_2m,precipitation"
HOUR_FIELDS_WIND = "wind_speed_10m,wind_direction_10m"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

# ==========================
# Utilidades
# ==========================
def now_tz() -> datetime:
    return datetime.now(TZ)

def to_hour_floor(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)

def parse_city(city: str) -> str:
    return city.strip().lower().replace(" ", "_")

def csv_path(city: str, prefix: str = "open_meteo") -> Path:
    return DATA_DIR / f"{prefix}_{parse_city(city)}.csv"

def load_existing(city: str) -> pd.DataFrame:
    path = csv_path(city)
    if path.exists():
        df = pd.read_csv(path)
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
        return df
    return pd.DataFrame()

def save_df(df: pd.DataFrame, city: str) -> str:
    if df.empty:
        return ""
    path = csv_path(city)
    tmp = path.with_suffix(".tmp.csv")
    df.sort_values("datetime", inplace=True)
    df.drop_duplicates(subset=["municipio", "datetime"], keep="last", inplace=True)
    df.to_csv(tmp, index=False)
    shutil.move(tmp, path)
    return str(path)

def normalize_df(df: pd.DataFrame, city: str) -> pd.DataFrame:
    if df.empty:
        return df
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["hour"] = df["datetime"].dt.hour
    df["date"] = df["datetime"].dt.date
    df["municipio"] = parse_city(city)
    return df

def filter_hours(df: pd.DataFrame, start_hour: int, end_hour: int) -> pd.DataFrame:
    if df.empty:
        return df
    return df[(df["hour"] >= start_hour) & (df["hour"] <= end_hour)]

def ymd(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def last_timestamp(df: pd.DataFrame) -> Optional[pd.Timestamp]:
    if df.empty:
        return None
    return pd.to_datetime(df["datetime"]).max()

# ==========================
# Descarga desde Open-Meteo
# ==========================
def fetch_archive(lat: float, lon: float, start_date: str, end_date: str, hourly_fields: str) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": hourly_fields,
        "timezone": "America/Bogota",
    }
    r = SESSION.get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "hourly" not in data or "time" not in data["hourly"]:
        return pd.DataFrame()
    df = pd.DataFrame({"datetime": data["hourly"]["time"]})
    for k, v in data["hourly"].items():
        if k != "time":
            df[k] = v
    return df

def fetch_forecast(lat: float, lon: float, hourly_fields: str, past_days: int = 3, forecast_days: int = 1) -> pd.DataFrame:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly_fields,
        "timezone": "America/Bogota",
        "past_days": past_days,
        "forecast_days": forecast_days,
    }
    r = SESSION.get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "hourly" not in data or "time" not in data["hourly"]:
        return pd.DataFrame()
    df = pd.DataFrame({"datetime": data["hourly"]["time"]})
    for k, v in data["hourly"].items():
        if k != "time":
            df[k] = v
    return df

# ==========================
# Manejo robusto con reintentos
# ==========================
def safe_fetch_archive(lat, lon, start_date, end_date, hourly_fields, retries=5) -> pd.DataFrame:
    for attempt in range(retries):
        try:
            return fetch_archive(lat, lon, start_date, end_date, hourly_fields)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                wait = (attempt + 1) * random.uniform(3, 6)
                print(f"⚠️ Rate limit alcanzado. Reintentando en {wait:.1f}s...")
                time.sleep(wait)
            else:
                raise
    print("❌ Error persistente al descargar datos.")
    return pd.DataFrame()

# ==========================
# Pull incremental
# ==========================
def incremental_pull(city: str,
                     lat: float,
                     lon: float,
                     start_hour: int,
                     end_hour: int,
                     wind_only: bool = False) -> dict:
    hourly_fields = HOUR_FIELDS_WIND if wind_only else HOUR_FIELDS_ALL
    city_norm = parse_city(city)

    existing = load_existing(city_norm)
    last_ts = last_timestamp(existing)
    now_local = now_tz()
    target_until = to_hour_floor(now_local)

    if last_ts is None:
        start_date = ymd(now_local - timedelta(days=5*365))
    else:
        start_date = ymd((last_ts + timedelta(hours=1)).to_pydatetime())

    end_date = ymd(target_until)

    archive_df = pd.DataFrame()
    yesterday = ymd(now_local - timedelta(days=1))
    if start_date <= yesterday:
        arch_end = min(yesterday, end_date)
        archive_df = safe_fetch_archive(lat, lon, start_date, arch_end, hourly_fields)

    forecast_df = fetch_forecast(lat, lon, hourly_fields, past_days=3, forecast_days=1)

    df_all = pd.concat([archive_df, forecast_df], ignore_index=True)
    if df_all.empty:
        merged = existing
        new_rows = 0
    else:
        df_all["datetime"] = pd.to_datetime(df_all["datetime"])
        df_all = normalize_df(df_all, city_norm)
        df_all = filter_hours(df_all, start_hour, end_hour)
        merged = pd.concat([existing, df_all], ignore_index=True)
        merged.drop_duplicates(subset=["municipio", "datetime"], keep="last", inplace=True)
        new_rows = len(merged) - len(existing)

    path = save_df(merged, city_norm)
    return {
        "city": city_norm,
        "new_rows": int(new_rows),
        "file": path,
        "last_timestamp": merged["datetime"].max().strftime("%Y-%m-%d %H:%M") if not merged.empty else None,
        "success": True,
    }

# ==========================
# Esquemas Pydantic
# ==========================
class UpdateRequest(BaseModel):
    city: Optional[str] = None
    start_hour: int = 0
    end_hour: int = 23
    wind_only: bool = False

# ==========================
# FastAPI
# ==========================
app = FastAPI(title="Guajira Climate API", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True, "time": now_tz().isoformat()}

@app.post("/update/hourly")
def update_hourly(req: UpdateRequest):
    cities = [parse_city(req.city)] if req.city else list(MUNICIPIOS.keys())
    results = []
    for c in cities:
        if c not in MUNICIPIOS:
            results.append({"city": c, "success": False, "error": "municipio desconocido"})
            continue
        lat, lon = MUNICIPIOS[c]
        try:
            res = incremental_pull(c, lat, lon, req.start_hour, req.end_hour, req.wind_only)
            results.append(res)
            time.sleep(0.3)
        except Exception as e:
            results.append({"city": c, "success": False, "error": str(e)})
    return {"updated": results}

# ==========================
# Bootstrap al iniciar API (últimos 5 años)
# ==========================
@app.on_event("startup")
def startup_event():
    """Descarga inicial (últimos 5 años en bloques de 6 meses)"""
    now_local = now_tz()
    start_date = now_local - timedelta(days=5*365)
    hourly_fields = HOUR_FIELDS_ALL

    for city, (lat, lon) in MUNICIPIOS.items():
        try:
            all_data = pd.DataFrame()
            current = start_date
            while current < now_local:
                block_end = min(current + timedelta(days=180), now_local)
                df = safe_fetch_archive(lat, lon, ymd(current), ymd(block_end), hourly_fields)
                df = normalize_df(df, city)
                df = filter_hours(df, 0, 23)
                all_data = pd.concat([all_data, df], ignore_index=True)
                current = block_end + timedelta(days=1)
                time.sleep(3)  # pausa entre requests
            if not all_data.empty:
                save_df(all_data, city)
                print(f"📥 {city}: descarga inicial completa ({len(all_data)} registros)")
        except Exception as e:
            print(f"❌ Error en descarga inicial de {city}: {e}")
    print("✅ Descarga inicial de 5 años completada.")

# ==========================
# Scheduler opcional
# ==========================
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger

    scheduler = BackgroundScheduler(timezone="America/Bogota")

    def scheduled_update():
        for c, (lat, lon) in MUNICIPIOS.items():
            try:
                incremental_pull(c, lat, lon, start_hour=0, end_hour=23, wind_only=False)
                time.sleep(0.3)
            except Exception:
                continue

    scheduler.add_job(scheduled_update, CronTrigger(minute=5))
    if os.getenv("ENABLE_SCHEDULER", "true").lower() in ("1", "true", "yes"):
        scheduler.start()
except Exception:
    pass
