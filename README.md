# Asteroid Tracker API 🚀

API REST que monitorea asteroides cercanos a la Tierra usando datos reales de NASA.

## Características
- Consigue datos de asteroides desde NASA NeoWs API
- Almacena en PostgreSQL
- Endpoints RESTful con FastAPI
- CORS habilitado para consumir desde frontend

## Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (Google Cloud SQL)
- **Deploy:** Google Cloud Run
- **API Externa:** NASA NeoWs API

## Endpoints
- `GET /` - Health check
- `GET /asteroides` - Obtiene todos los asteroides
- `GET /asteroides/{id}` - Obtiene un asteroide por ID

## Ejemplo de respuesta
```json
{
  "total": 6,
  "asteroides": [
    {
      "id": 1,
      "nombre": "Apophis",
      "tamaño_km": 0.37,
      "fecha_deteccion": "2026-05-25",
      "peligroso": true
    }
  ]
}
```

## Deployment
Desplegado en Google Cloud Run: https://asteroides-api-979143368634.europe-west1.run.app

## Autor
Jesús Pérez - Aprendiendo Full Stack Development