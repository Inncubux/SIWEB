import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Base de la URL
url_base = "https://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form"

# Parámetros comunes
params = {
    "itype": "ymd", "yr": 1976, "mo": 1, "day": 1,
    "otype": "ymd", "oyr": 2025, "omo": 5, "oday": 23,
    "jyr": 1976, "jday": 1, "ojyr": 1976, "ojday": 1,
    "nday": 1, "lmw": 0, "umw": 10, "lms": 0, "ums": 10,
    "lmb": 0, "umb": 10, "llat": -90, "ulat": 90,
    "llon": -180, "ulon": 180, "lhd": 0, "uhd": 1000,
    "lts": -9999, "uts": 9999, "lpe1": 0, "upe1": 90,
    "lpe2": 0, "upe2": 90, "list": 0
}

datos = []
start = 0

while True:
    print(f"🔎 Procesando página con start={start}...")
    params["start"] = start
    resp = requests.get(url_base, params=params)
    soup = BeautifulSoup(resp.text, "html.parser")
    bloques = soup.find_all("pre")

    if not bloques:
        print("✅ No hay más resultados. Fin del scraping.")
        break

    for pre in bloques:
        texto = pre.get_text()

        try:
            fecha = re.search(r'Date:\s*(\d{4}/\s*\d+/\s*\d+)', texto).group(1).replace(' ', '')
            hora = re.search(r'Centroid Time:\s*([\d:.]+)', texto).group(1)
            lat = float(re.search(r'Lat=\s*([-\d.]+)', texto).group(1))
            lon = float(re.search(r'Lon=\s*([-\d.]+)', texto).group(1))
            prof = float(re.search(r'Depth=\s*([-\d.]+)', texto).group(1))
            mw = float(re.search(r'Mw\s*=\s*([-\d.]+)', texto).group(1))
            mb = float(re.search(r'mb\s*=\s*([-\d.]+)', texto).group(1))
            ms = float(re.search(r'Ms\s*=\s*([-\d.]+)', texto).group(1))
            scalar_moment = re.search(r'Scalar Moment\s*=\s*([\deE\+\.-]+)', texto).group(1)

            # Extraer los dos planes de falla
            fault_planes = re.findall(r'strike=([-\d.]+)\s+dip=([-\d.]+)\s+slip=([-\d.]+)', texto)
            strike1, dip1, slip1 = fault_planes[0] if len(fault_planes) > 0 else (None, None, None)
            strike2, dip2, slip2 = fault_planes[1] if len(fault_planes) > 1 else (None, None, None)

            datos.append({
                "Fecha": fecha,
                "Hora": hora,
                "Latitud": lat,
                "Longitud": lon,
                "Profundidad (km)": prof,
                "Magnitud Mw": mw,
                "Magnitud mb": mb,
                "Magnitud Ms": ms,
                "Scalar Moment": scalar_moment,
                "Strike1": strike1,
                "Dip1": dip1,
                "Slip1": slip1,
                "Strike2": strike2,
                "Dip2": dip2,
                "Slip2": slip2,
                "Pagina start": start
            })

        except Exception as e:
            print(f"⚠️ Error procesando un bloque: {e}")

    start += 9
    if start == 18:  # Limitar el número de páginas para evitar sobrecargar el servidor
        print("⚠️ Se ha alcanzado el límite de páginas. Fin del scraping.")
        break
    time.sleep(1)  # evitar sobrecargar el servidor

# Guardar resultados
df = pd.DataFrame(datos)
df.to_excel("eventos_CMT_global_todos.xlsx", index=False)
print("✅ Archivo Excel guardado como 'eventos_CMT_global_todos.xlsx'")
