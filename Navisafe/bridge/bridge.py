#!/usr/bin/env python3
"""
Navisafe — Python Bridge (API REST Flask)
Autors: Miquel Calzada, Guillem Tarradas · Institut de Palamós · SMX2 · 2026

Instal·lació: pip3 install flask flask-cors
Ús:           python3 bridge.py
"""
import os, json, time
from flask import Flask, jsonify
from flask_cors import CORS

DATA_DIR = "/tmp/navisafe"
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

def read(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {"status": "NO_DATA", "sensor": filename.replace(".json","")}
    try:
        with open(path) as f:
            d = json.load(f)
        if time.time() - d.get("timestamp", 0) > 10:
            d["status"] = "STALE"
        return d
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def ok(data):
    r = jsonify(data)
    r.headers["Cache-Control"] = "no-cache"
    return r

@app.route("/api/status")
def status():
    return ok({"status":"OK","service":"Navisafe Bridge",
                "timestamp":time.time(),"time_str":time.strftime("%H:%M:%S")})

@app.route("/api/gps")
def gps():    return ok(read("gps_sensor.json"))

@app.route("/api/fuel")
def fuel():   return ok(read("fuel_sensor.json"))

@app.route("/api/engine")
def engine(): return ok(read("engine_temp_sensor.json"))

@app.route("/api/ais")
def ais():    return ok(read("ais_sensor.json"))

@app.route("/api/water")
def water():  return ok(read("water_sensor.json"))

@app.route("/api/camera")
def camera(): return ok(read("camera_node.json"))

@app.route("/api/alerts")
def alerts():
    path = os.path.join(DATA_DIR, "alerts.json")
    if not os.path.exists(path): return ok([])
    try:
        with open(path) as f: return ok(json.load(f)[-20:])
    except: return ok([])

@app.route("/api/all")
def all_data():
    alerts_data = []
    path = os.path.join(DATA_DIR, "alerts.json")
    if os.path.exists(path):
        try:
            with open(path) as f: alerts_data = json.load(f)[-10:]
        except: pass
    return ok({
        "gps":      read("gps_sensor.json"),
        "fuel":     read("fuel_sensor.json"),
        "engine":   read("engine_temp_sensor.json"),
        "ais":      read("ais_sensor.json"),
        "water":    read("water_sensor.json"),
        "camera":   read("camera_node.json"),
        "alerts":   alerts_data,
        "timestamp": time.time(),
        "time_str":  time.strftime("%H:%M:%S"),
    })

if __name__ == "__main__":
    print("=" * 45)
    print("  NAVISAFE — API Bridge :5000")
    print("  http://0.0.0.0:5000/api/all")
    print("=" * 45)
    app.run(host="0.0.0.0", port=5000, debug=False)