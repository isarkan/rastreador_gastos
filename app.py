import argparse
import json
import os
import csv
from datetime import datetime

ARCHIVO = "gastos.json"

def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return {"gastos": [], "presupuestos": {}}

    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)
    
    