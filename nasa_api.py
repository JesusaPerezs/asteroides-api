import requests
from datetime import datetime, timedelta
import json

API_KEY = "7jbsV0OngpFDj914VZK1D2pP3MemnddghSmkl6TQ"

hoy = datetime.now().strftime("%Y-%m-%d")
mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={hoy}&end_date={mañana}&api_key={API_KEY}"

response = requests.get(url)
datos = response.json()

print(f"Asteroides cercanos entre hoy: {hoy} y mañana: {mañana}")
print(f"Total: {datos["element_count"]}\n")

for fecha, asteroides in datos["near_earth_objects"].items():
    print(f"fecha: {len(asteroides)} asteroides")
    for ast in asteroides[:3]:
        nombre = ast["name"]
        tamaño = ast["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
        peligroso = ast["is_potentially_hazardous_asteroid"]
        print(f" - nombre: {nombre}, tamaño: {tamaño:.2f} km, Peligroso: {peligroso}")

#with open("asteroides.json", "w") as f:
 #   json.dump(datos["near_earth_objects"], f, indent=2)
#print("\n Datos guardado en asteroides.json correctamente")