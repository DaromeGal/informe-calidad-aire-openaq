import json
from pathlib import Path


DATA_PATH = Path("data.json")
README_PATH = Path("README.md")


def cargar_datos():
    if not DATA_PATH.exists():
        return None
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generar_tabla(medidas):
    if not medidas:
        return "No hay medidas disponibles.\n"


    # Tomamos las 5 primeras para la tabla
    top = medidas[:5]


    lineas = [
        "| Fecha (UTC) | Valor PM2.5 | Latitud | Longitud | Sensor ID | Location ID |",
        "|-------------|-------------|---------|----------|-----------|------------|",
    ]


    for m in top:
        lineas.append(
            f"| {m.get('datetime_utc', '-')}"
            f" | {m.get('value', '-')}"
            f" | {m.get('latitude', '-')}"
            f" | {m.get('longitude', '-')}"
            f" | {m.get('sensors_id', '-')}"
            f" | {m.get('locations_id', '-')}"
            f" |"
        )


    return "\n".join(lineas) + "\n"


def generar_readme(datos):
    if not datos:
        contenido = "# Informe de calidad del aire 🌍\n\nNo hay datos todavía."
    else:
        fecha = datos.get("fecha_generacion_utc", "desconocida")
        param = datos.get("parametro", "desconocido")
        total = datos.get("total_medidas", 0)
        medidas = datos.get("medidas", [])


        tabla = generar_tabla(medidas)


    contenido = f"""# Informe automático de calidad del aire 🌍

Este informe se genera automáticamente usando **Python**, **OpenAQ v3** y **GitHub Actions**.

## Última actualización

- Fecha de generación (UTC): `{fecha}`
- Parámetro: `{param}`
- Número de medidas obtenidas: `{total}`

## Muestra de las últimas medidas (máx. 5)

{tabla}
---

_Repositorio mantenido automáticamente por GitHub Actions._
"""



    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(contenido)


if __name__ == "__main__":
    datos = cargar_datos()
    generar_readme(datos)
    print("README.md actualizado.")
