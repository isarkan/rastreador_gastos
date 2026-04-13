from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
ARCHIVO = "gastos.json"


def cargar_gastos():
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_gastos(gastos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)


def generar_id(gastos):
    return max([g["id"] for g in gastos], default=0) + 1


@app.route("/")
def index():
    gastos = cargar_gastos()
    total = sum(g["monto"] for g in gastos)
    return render_template("index.html", gastos=gastos, total=total)


@app.route("/add", methods=["POST"])
def add_gasto():
    gastos = cargar_gastos()

    nuevo = {
        "id": generar_id(gastos),
        "descripcion": request.form["descripcion"],
        "monto": float(request.form["monto"]),
        "categoria": request.form.get("categoria") or "General",
        "fecha": datetime.now().strftime("%Y-%m-%d")
    }

    gastos.append(nuevo)
    guardar_gastos(gastos)

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_gasto(id):
    gastos = [g for g in cargar_gastos() if g["id"] != id]
    guardar_gastos(gastos)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)