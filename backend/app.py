from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import pandas as pd
import requests
from process import process_data_fwt, process_data_macro, process_data_tensile, process_data_chem

# --- API Setup ---
app = FastAPI()

# Dynamically resolve absolute path to the downloads directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_PATH = os.path.join(APP_ROOT, 'downloads')
os.makedirs(DOWNLOADS_PATH, exist_ok=True)

print(f"Downloads directory resolved to: {DOWNLOADS_PATH}")

# Mount static files for downloads
app.mount("/api/download", StaticFiles(directory=DOWNLOADS_PATH), name="downloads")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Config ---
LOGIN_URL = "https://bspapp.sail-bhilaisteel.com/setu/api/token/"
CREDENTIALS = {
    "username": "ritesuser",
    "password": "bsprites1234#"
}

API_ENDPOINTS = {
    "fwt": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_fwt/",
    "macro": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_macro/",
    "chem": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_chem/",
    "tensile": "https://bspapp.sail-bhilaisteel.com/setu/public_api/shift_tensile/"
}

class DateRequest(BaseModel):
    date: str


@app.get("/api/download-file/{filename}")
def download_file(filename: str):
    file_path = os.path.join(DOWNLOADS_PATH, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')


@app.post("/api/fetch-data")
def fetch_data(request: DateRequest):
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
            elif api_name == 'chem':
                df_rsm , df_urm = process_data_chem (df)
                print(f"Processed chem dataframes - RSM shape: {df_rsm.shape}, URM shape: {df_urm.shape}")
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

            files_created.extend([filename_rsm, filename_urm])

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
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            return data
        except Exception as e:
            print(f"JSON decode error for {url}: {e}")
            return None
    return None


@app.get("/api/list-files")
def list_files():
    print(f"Listing files in directory: {DOWNLOADS_PATH}")
    try:
        files = [
            f for f in os.listdir(DOWNLOADS_PATH)
            if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))
        ]
        print(f"Files found: {files}")
        return {"files": files}
    except Exception as e:
        print(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail="Could not list files")


@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>FastAPI backend running</h2>"


# --- Run with: uvicorn app:app --reload --port 5000 ---
