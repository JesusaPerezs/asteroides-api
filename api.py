from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timedelta

app = FastAPI(title="AsteroidesAPI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def get_bd_connection():
        return psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )

@app.get("/asteroides")
def get_asteroides():
    conn = get_bd_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asteroides")
    asteroides = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"total": len(asteroides), "asteroides": asteroides}

@app.get("/asteroides/{id}")
def get_asteroide(id: int):
    conn = get_bd_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asteroides WHERE id = %s", (id,))
    asteroide = cursor.fetchone()
    cursor.close()
    conn.close()
    return asteroide


@app.get("/")
def health():
    return {"Status": "API Funcionando correctamente"}

@app.post("/asteroides/fetch")
def call_NASA():
     
     hoy = datetime.now().strftime("%Y-%m-%d")
     mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

     API_KEY = os.getenv("NASA_API_KEY")

     url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={hoy}&end_date={mañana}&api_key={API_KEY}"
     response = requests.get(url)
     datos = response.json()

     conn = get_bd_connection()    # ← antes del loop
     cursor = conn.cursor()

     for fecha, asteroides in datos["near_earth_objects"].items():
        print(f"fecha: {len(asteroides)} asteroides")
        for ast in asteroides[:3]:
             nombre = ast["name"]
             tamaño = ast["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
             insertar = "INSERT INTO asteroides (nombre, tamaño_km, fecha_deteccion, peligroso) VALUES (%s, %s, %s, %s)"
             cursor.execute(insertar, (nombre, tamaño, fecha, True))
             print(f" - nombre: {nombre}, tamaño: {tamaño:.2f} km")
     conn.commit()
     cursor.close()
     conn.close()
     return {"mensaje": "Asteroides insertados correctamente"}