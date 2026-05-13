#!/usr/bin/env python3
"""
Navisafe - Sensors simulats
Autors: Miquel Calzada, Guillem Tarradas - Institut de Palamós - SMX2 2026
 
Ús: python3 sensors_demo.py
"""
import random, math, time, json, os
 
DATA_DIR = "/tmp/navisafe"
os.makedirs(DATA_DIR, exist_ok=True)
 
lat, lon = 41.84778, 3.13497
angle, radius = random.uniform(0, 360), 2.0
fuel, temp, sent = 80.0, 72.0, 8.0
trail = []
 
VESSELS = ['COSTA BRAVA I', 'PESCADOR EMPORDÀ', 'PONENT', 'TRAMUNTANA', 'CAP DE BEGUR']
 
def simular():
    global lat, lon, angle, radius, fuel, temp, sent, trail
 
    # Límits zona marítima
    MIN_LAT = 41.84775  # zona submarinisme Palamós
    MAX_LAT = 41.84782  # Torre Valentina
    MIN_LON = 3.13490   # zona submarinisme Palamós
    MAX_LON = 3.13505   # Torre Valentina
 
    # Moviment petit aleatori
    lat += random.uniform(-0.00002, 0.00002)
    lon += random.uniform(-0.00002, 0.00002)
 
    # Limitar dins la zona
    lat = round(max(MIN_LAT, min(MAX_LAT, lat)), 6)
    lon = round(max(MIN_LON, min(MAX_LON, lon)), 6)
 
    trail.append({"lat": lat, "lon": lon})
    trail[:] = trail[-15:]
 
    fuel  = max(0,   round(fuel - random.uniform(0, 0.2),  1))
    temp  = max(60,  min(round(temp + random.uniform(-1.5, 2.5), 1), 115))
    sent  = max(0,   min(round(sent + random.uniform(-1.0, 2.0), 1), 100))
    vel   = round(random.uniform(0.5, 8.0), 1)
    rumb  = round((angle + 90) % 360)
    n_ais = random.randint(0, 4)
    vessels = random.sample(VESSELS, n_ais)
    cam_ok  = random.random() > 0.1
 
    alertes = []
    ts = time.strftime("%H:%M:%S")
    if fuel < 20:
        alertes.append({"nivell": "WARNING",  "msg": f"⛽ Combustible baix: {fuel}%",   "hora": ts})
    if temp > 100:
        alertes.append({"nivell": "CRITICAL", "msg": f"🌡️ Temperatura motor: {temp}°C", "hora": ts})
    if sent > 25:
        alertes.append({"nivell": "CRITICAL", "msg": f"💧 Bomba sentina: {sent}%",      "hora": ts})
    if fuel < 10 and alertes:
        alertes[0]["nivell"] = "CRITICAL"
 
    dades = {
        "gps":     {"lat": lat, "lon": lon, "trail": trail, "velocitat": vel, "rumb": rumb},
        "fuel":    {"valor": fuel,  "estat": "CRITICAL" if fuel < 10 else "WARNING" if fuel < 20 else "OK"},
        "motor":   {"valor": temp,  "estat": "CRITICAL" if temp > 100 else "WARNING" if temp > 90 else "OK"},
        "sentina": {"valor": sent,  "estat": "CRITICAL" if sent > 25 else "WARNING" if sent > 15 else "OK"},
        "ais":     {"vaixells": n_ais, "llista": vessels},
        "camera":  {"ok": cam_ok},
        "alertes": alertes,
        "hora":    ts,
    }
 
    with open(f"{DATA_DIR}/dades.json", "w") as f:
        json.dump(dades, f)
 
    print(f"[{ts}] GPS:{lat},{lon} | Fuel:{fuel}% | Temp:{temp}°C | Sent:{sent}% | AIS:{n_ais} | Cam:{'OK' if cam_ok else 'ERR'}")
 
print("Navisafe - Sensors en marxa. Ctrl+C per aturar.")
while True:
    simular()
    time.sleep(1)