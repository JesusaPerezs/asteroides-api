nombre_asteroide = "Apophis"
tamaño_km = 0.37
asteroides_detectados = 2847
es_peligroso = True

print(f"Asteroide: {nombre_asteroide}")
print(f"Tamaño: {tamaño_km} km")
print(f"Detectados hoy: {asteroides_detectados}")
print(f"¿Es peligroso? {es_peligroso}")

def es_peligroso(tamaño):
    if tamaño > 0.14:
        return True
    else:
        False

function_1 = es_peligroso(30)
function_2 = es_peligroso(0.2)

print(f"El meteorito Alphet es peligroso?:{function_1} ")
print(f"El meteorito kk es peligroso?:{function_2} ")


asteroides = ["Apophis", "Bennu", "2022 AP7", "Eros"]

print("Asteroides detectados:")
for asteroide in asteroides:
    print(f"  - {asteroide}")

asteroide_info = {
    "nombre": "Apophis",
    "tamaño_km": 0.37,
    "distancia_km": 7980000,
    "peligroso": True
}

print(f"\nInfo de {asteroide_info['nombre']}:")
print(f"  Tamaño: {asteroide_info['tamaño_km']} km")
print(f"  Distancia: {asteroide_info['distancia_km']} km")
print(f"  ¿Peligroso? {asteroide_info['peligroso']}")


# LISTA DE DICCIONARIOS - Los asteroides reales que traeremos de NASA

asteroides_lista = [
    {
        "nombre": "Apophis",
        "tamaño_km": 0.37,
        "peligroso": True
    },
    {
        "nombre": "Bennu",
        "tamaño_km": 0.24,
        "peligroso": True
    },
    {
        "nombre": "Eros",
        "tamaño_km": 0.17,
        "peligroso": True
    }
]

# Recorremos todos los asteroides
for ast in asteroides_lista:
    estado = "⚠️ PELIGROSO" if ast["peligroso"] else "✅ Seguro"
    print(f"{ast['nombre']}: {ast['tamaño_km']} km - {estado}")