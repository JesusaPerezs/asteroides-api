import psycopg2
import json
from datetime import datetime

conexion = psycopg2.connect(
    host = "35.254.215.53",
    database = "postgres",
    user = "postgres",
    password = "Parisina2324**"
)

cursor = conexion.cursor()

create_tabla = """
CREATE TABLE IF NOT EXISTS asteroides(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    tamaño_km FLOAT,
    fecha_deteccion DATE,
    peligroso BOOLEAN,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
    )
"""

cursor.execute(create_tabla)
conexion.commit()
print("Tabla creada correctamente")

with open("asteroides.json", "r") as f:
    datos = json.load(f)

for fecha, asteroides in datos.items():
    for ast in asteroides[:3]:
        nombre = ast["name"]
        tamaño = ast["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
        
        insertar = "INSERT INTO asteroides (nombre, tamaño_km, fecha_deteccion, peligroso) VALUES (%s, %s, %s, %s)"
        cursor.execute(insertar, (nombre, tamaño, fecha, True))

conexion.commit()
cursor.close()
conexion.close()