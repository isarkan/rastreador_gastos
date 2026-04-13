import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

ARCHIVO = "gastos.json"


def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_datos(gastos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)


class AppGastos:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Rastreador de Gastos")
        self.root.geometry("900x550")

        self.gastos = cargar_datos()
        self.gasto_seleccionado = None

        self.crear_ui()
        self.refrescar_tabla()
        self.actualizar_resumen()

    def crear_ui(self):
        frame_top = tk.Frame(self.root, padx=10, pady=10)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Descripción").grid(row=0, column=0)
        self.entry_desc = tk.Entry(frame_top, width=30)
        self.entry_desc.grid(row=0, column=1, padx=5)

        tk.Label(frame_top, text="Monto").grid(row=0, column=2)
        self.entry_monto = tk.Entry(frame_top, width=15)
        self.entry_monto.grid(row=0, column=3, padx=5)

        tk.Label(frame_top, text="Categoría").grid(row=0, column=4)
        self.entry_cat = tk.Entry(frame_top, width=20)
        self.entry_cat.grid(row=0, column=5, padx=5)

        tk.Button(frame_top, text="Agregar", command=self.agregar_gasto).grid(row=0, column=6, padx=5)
        tk.Button(frame_top, text="Actualizar", command=self.actualizar_gasto).grid(row=0, column=7, padx=5)
        tk.Button(frame_top, text="Eliminar", command=self.eliminar_gasto).grid(row=0, column=8, padx=5)

        columnas = ("id", "descripcion", "monto", "categoria", "fecha")
        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=18)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)

        self.tabla.column("id", width=60)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_gasto)

        frame_bottom = tk.Frame(self.root, padx=10, pady=10)
        frame_bottom.pack(fill="x")

        self.label_total = tk.Label(frame_bottom, text="Total: $0", font=("Arial", 12, "bold"))
        self.label_total.pack(side="left")

    def generar_id(self):
        if not self.gastos:
            return 1
        return max(g["id"] for g in self.gastos) + 1

    def agregar_gasto(self):
        desc = self.entry_desc.get().strip()
        monto_txt = self.entry_monto.get().strip()
        cat = self.entry_cat.get().strip() or "General"

        if not desc or not monto_txt:
            messagebox.showerror("Error", "Descripción y monto son obligatorios")
            return

        try:
            monto = float(monto_txt)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
            return

        nuevo = {
            "id": self.generar_id(),
            "descripcion": desc,
            "monto": monto,
            "categoria": cat,
            "fecha": datetime.now().strftime("%Y-%m-%d")
        }

        self.gastos.append(nuevo)
        guardar_datos(self.gastos)
        self.limpiar_campos()
        self.refrescar_tabla()
        self.actualizar_resumen()

    def seleccionar_gasto(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]
        self.gasto_seleccionado = valores[0]

        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, valores[1])

        self.entry_monto.delete(0, tk.END)
        self.entry_monto.insert(0, valores[2])

        self.entry_cat.delete(0, tk.END)
        self.entry_cat.insert(0, valores[3])

    def actualizar_gasto(self):
        if self.gasto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un gasto")
            return

        try:
            monto = float(self.entry_monto.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
            return

        for gasto in self.gastos:
            if gasto["id"] == self.gasto_seleccionado:
                gasto["descripcion"] = self.entry_desc.get().strip()
                gasto["monto"] = monto
                gasto["categoria"] = self.entry_cat.get().strip() or "General"
                break

        guardar_datos(self.gastos)
        self.limpiar_campos()
        self.refrescar_tabla()
        self.actualizar_resumen()

    def eliminar_gasto(self):
        if self.gasto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un gasto")
            return

        self.gastos = [g for g in self.gastos if g["id"] != self.gasto_seleccionado]
        guardar_datos(self.gastos)
        self.gasto_seleccionado = None
        self.limpiar_campos()
        self.refrescar_tabla()
        self.actualizar_resumen()

    def refrescar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for gasto in self.gastos:
            self.tabla.insert("", tk.END, values=(
                gasto["id"],
                gasto["descripcion"],
                gasto["monto"],
                gasto["categoria"],
                gasto["fecha"],
            ))

    def actualizar_resumen(self):
        total = sum(g["monto"] for g in self.gastos)
        self.label_total.config(text=f"💰 Total gastado: ${total:,.2f}")

    def limpiar_campos(self):
        self.entry_desc.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.entry_cat.delete(0, tk.END)
        self.gasto_seleccionado = None


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGastos(root)
    root.mainloop()
