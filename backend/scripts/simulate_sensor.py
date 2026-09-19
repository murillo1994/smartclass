"""
Script de Simulação de Hardware IoT (ESP32) para o SmartClass
Envia leituras periódicas de telemetria térmica para validação do endpoint POST /api/v1/medicoes.
"""

import time
import random
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1/medicoes")
SALAS = ["Sala 101", "Sala 102", "Laboratorio-01", "Auditorio"]

def simulate_reading(sala_id: str, include_humidity: bool = True):
    # Gera valores realistas de temperatura (18°C a 30°C) e umidade (40% a 80%)
    temperatura = round(random.uniform(18.5, 29.5), 2)
    payload = {
        "sala_id": sala_id,
        "temperatura": temperatura
    }
    if include_humidity:
        payload["umidade"] = round(random.uniform(45.0, 75.0), 2)

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        print(f"[{time.strftime('%X')}] POST {API_URL} -> Status: {response.status_code} | Resposta: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"[{time.strftime('%X')}] Erro ao conectar na API ({API_URL}): {e}")

if __name__ == "__main__":
    print(f"Iniciando simulação de telemetria ESP32 -> {API_URL}")
    print("Pressione Ctrl+C para encerrar.")
    try:
        while True:
            for sala in SALAS:
                simulate_reading(sala, include_humidity=random.choice([True, False]))
                time.sleep(1)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSimulação encerrada.")
