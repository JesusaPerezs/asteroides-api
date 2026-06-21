from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor # hace que los resultados lleguen como diccionarios
import os # Se conecta al sistema operativo donde corre tu código
from fastapi.middleware.cors import CORSMiddleware # Es el guardia de seguridad que controla qué dominios pueden llamar tu API. 
import requests
from datetime import datetime, timedelta

app = FastAPI(title="AsteroidesAPI", version="1.0") # creación de la aplicaciónn

app.add_middleware( # agregarle una capa a tu app. Imagina que tu API es un restaurante y el middleware es el guardia en la puerta
    CORSMiddleware,
    allow_origins=["*"], # deja entrar a CUALQUIER dominio
    allow_credentials=True, # acepta cookies y tokens
    allow_methods = ["*"], # acepta GET, POST, PUT, DELETE
    allow_headers = ["*"], # acepta cualquier header: solo para leer o mandar requests
)

def get_bd_connection():
        return psycopg2.connect(
            host = os.getenv("DB_HOST"), # va al sistema operativo de Cloud Run y busca el valor de cada variable. 
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
        )

@app.get("/asteroides")
def get_asteroides():
    conn = get_bd_connection() # conexión abierta a PostgreSQL
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asteroides") # panel donde escribes y ejecutas queries.
    asteroides = cursor.fetchall() # los resultados están listos pero no en Python todavía. fetchall() los jala todos y los guarda en la variable asteroides
    cursor.close() # cierran el panel y la llamada
    conn.close()
    return {"total": len(asteroides), "asteroides": asteroides}

@app.get("/asteroides/{id}")
def get_asteroide(id: int):
    conn = get_bd_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM asteroides WHERE id = %s", (id,))
    asteroide = cursor.fetchone() # es lo mismo pero solo trae un registro
    cursor.close()
    conn.close()
    return asteroide


@app.get("/")
def health():
    return {"Status": "API Funcionando correctamente"}

@app.post("/asteroides/fetch") # POST significa que alguien de afuera llama este endpoint para que tu API haga algo 
def call_NASA():
     
     hoy = datetime.now().strftime("%Y-%m-%d")
     mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

     API_KEY = os.getenv("NASA_API_KEY")

     url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={hoy}&end_date={mañana}&api_key={API_KEY}" # URL que la NASA definió para consultar asteroides cercanos. 
     response = requests.get(url)
     datos = response.json()

     conn = get_bd_connection() # abre la llamada
     cursor = conn.cursor() # alguien contesta y está listo

     for fecha, asteroides in datos["near_earth_objects"].items():
        print(f"fecha: {len(asteroides)} asteroides")
        for ast in asteroides[:3]:
             nombre = ast["name"]
             tamaño_km = ast["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
             peligroso = ast["is_potentially_hazardous_asteroid"]
             nasa_url = ast["nasa_jpl_url"]
             velocidad_km_hours = ast["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
             fecha_mayor_proximidad = ast["close_approach_data"][0]["close_approach_date"]
             distancia_mayor_proximidad = ast["close_approach_data"][0]["miss_distance"]["kilometers"]
             magnitud = ast["absolute_magnitude_h"]
             insertar = "INSERT INTO asteroides (nombre, tamaño_km, fecha_deteccion, peligroso, nasa_url, " \
             "velocidad_km_hours, fecha_mayor_proximidad, distancia_mayor_proximidad, " \
             "magnitud) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
             # %s son placeholders, espacios en blanco que psycopg2 rellena con los valores reales de forma segura
             cursor.execute(insertar, (nombre, tamaño_km, fecha, peligroso, nasa_url,
                                       velocidad_km_hours, fecha_mayor_proximidad, distancia_mayor_proximidad, magnitud))
     conn.commit() # confirmar y guardar permanentemente los cambios en PostgreSQL
     cursor.close()
     conn.close()
     return {"mensaje": "Asteroides insertados correctamente"}

@app.get("/foto") 
def get_image():
    API_KEY = os.getenv("NASA_API_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        fecha = datos["date"]
        explicacion = datos["explanation"]
        link = datos["hdurl"]
        return {"fecha": fecha, "explicacion": explicacion, "link": link}
    else:
        return {"error": response.status_code}