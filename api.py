from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="AsteroidesAPI", version="1.0")

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

@app.get("/asteroides")
def get_asteroides(id: int):
    conn = get_bd_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asteroides WHERE id = %s", (id))
    asteroide = cursor.fetchall()
    cursor.close()
    conn.close()
    return asteroide


@app.get("/")
def health():
    return {"Status": "API Funcionando correctamente"}