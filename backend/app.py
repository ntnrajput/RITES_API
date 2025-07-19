#  Start APP - uvicorn app:app --reload --port 5000

from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import pandas as pd
import requests
from process import process_data_fwt, process_data_macro, process_data_tensile
from fastapi.staticfiles import StaticFiles

# --- API Setup ---
app = FastAPI()
DOWNLOADS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOADS_PATH, exist_ok=True)
app.mount("/api/download", StaticFiles(directory=DOWNLOADS_PATH), name="downloads")

# CORS (allow frontend dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure downloads folder exists


# Static files for download
app.mount("/api/download", StaticFiles(directory=DOWNLOADS_PATH), name="downloads")

# --- API Details ---
LOGIN_URL = "https://bspapp.sail-bhilaisteel.com/setu/api/token/"
CREDENTIALS = {
    "username": "ritesuser",
    "password": "bsprites1234#"
}

API_ENDPOINTS = {
    # "fwt": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_fwt/",
    # "macro": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_macro/",
    # "chem": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_chem/",
    "tensile": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_tensile/"
}

class DateRequest(BaseModel):
    date: str


# --- The main API endpoint ---
@app.post("/api/fetch-data")
def fetch_data(request: DateRequest):
    # Get token
    token = get_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    files_created = []
    for api_name, endpoint in API_ENDPOINTS.items():
        data = fetch_api_data(endpoint, request.date, token)
        print(f"API: {api_name}, Data fetched: {len(data) if data else 0} records")
        if data:
            df = pd.DataFrame(data)
            if api_name == 'fwt':
                df_rsm, df_urm = process_data_fwt(df)
            elif api_name == 'macro':
                df_rsm, df_urm = process_data_macro(df)
            elif api_name == 'tensile':
                df_rsm, df_urm = process_data_tensile(df)
            else:
                continue
            print(f"Processed {api_name} - RSM rows: {len(df_rsm)}, URM rows: {len(df_urm)}")

            filename_rsm = f"RSM_{api_name}_{request.date}.xlsx"
            filename_urm = f"URM_{api_name}_{request.date}.xlsx"
            filepath_rsm = os.path.join(DOWNLOADS_PATH, filename_rsm)
            filepath_urm = os.path.join(DOWNLOADS_PATH, filename_urm)
            df_rsm.to_excel(filepath_rsm, index=False, engine="openpyxl")
            df_urm.to_excel(filepath_urm, index=False, engine="openpyxl")
            print(f"Saved file: {filepath_rsm}")
            print(f"Saved file: {filepath_urm}")
            files_created.append(filename_rsm)
            files_created.append(filename_urm)
    
    print("Files created:", files_created)
    return {
        "success": True,
        "message": f"Data fetched and files generated for {request.date}",
        "files_created": files_created
    }


def get_access_token():
    try:
        response = requests.post(LOGIN_URL, json=CREDENTIALS)
        if response.ok:
            return response.json().get("access")
    except Exception as e:
        print("Login error:", e)
    return None


def fetch_api_data(endpoint, date, token):
    url = f"{endpoint}{date}/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        try:
            data = response.json()
            # Handle case where API response is not a list/dict for DataFrame
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            return data
        except Exception as e:
            print(f"JSON decode error for {url}: {e}")
            return None
    return None

# (Optional) List files endpoint
@app.get("/api/list-files")
def list_files():
    files = [
        f for f in os.listdir(DOWNLOADS_PATH)
        if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))
    ]
    return {"files": files}

# Optional: Nice homepage
from fastapi.responses import HTMLResponse
@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>FastAPI backend running</h2>"

# --- Run with: uvicorn app:app --reload --port 5000 ---
