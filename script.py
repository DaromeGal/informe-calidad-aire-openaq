import json
import os
from datetime import datetime


import requests


API_URL = "https://api.openaq.org/v3/parameters/2/latest"  # PM2.5
LIMIT = 10  # número de registros que queremos


def obtener_api_key() -> str:
    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No se ha encontrado la variable de entorno OPENAQ_API_KEY.\n"
            "Configúrala en tu entorno local o como secret en GitHub Actions."
        )
    return api_key


def obtener_datos():
    api_key = obtener_api_key()


    params = {
        "limit": LIMIT,
    }


    headers = {
        "X-API-Key": api_key
    }


    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()


    resultados = data.get("results", [])


    medidas = []
    for item in resultados:
        medidas.append({
            "datetime_utc": item.get("datetime", {}).get("utc"),
            "value": item.get("value"),
            "latitude": item.get("coordinates", {}).get("latitude"),
            "longitude": item.get("coordinates", {}).get("longitude"),
            "sensors_id": item.get("sensorsId"),
            "locations_id": item.get("locationsId"),
        })


    resumen = {
        "fecha_generacion_utc": datetime.utcnow().isoformat(),
        "parametro": "PM2.5",
        "total_medidas": len(medidas),
        "medidas": medidas,
    }
    return resumen


def guardar_en_json(info, ruta="data.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    datos = obtener_datos()
    guardar_en_json(datos)
    print("Datos guardados en data.json")
