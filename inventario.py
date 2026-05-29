import tkinter as tk
from tkinter import ttk
import sqlite3

def crear_frame_inventario(frame):

    conexion = sqlite3.connect("productos.db")

    cursor = conexion.cursor()

    tk.Label(
        frame,
        text="INVENTARIO GENERAL",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    columnas = (
        "ID",
        "Nombre",
        "Dosis",
        "Lote",
        "Caducidad",
        "Fabricante",
        "Stock"
    )

    tabla = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings"
    )

    for col in columnas:

        tabla.heading(col, text=col)

        tabla.column(
            col,
            width=150
        )

    tabla.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # =====================================
    # CARGAR DATOS
    # =====================================

    def cargar_datos():

        for fila in tabla.get_children():
            tabla.delete(fila)

        cursor.execute(
            "SELECT * FROM productos"
        )

        productos = cursor.fetchall()

        for producto in productos:

            tabla.insert(
                "",
                "end",
                values=producto
            )

    cargar_datos()

    # =====================================
    # BOTON RECARGAR
    # =====================================

    tk.Button(
        frame,
        text="RECARGAR INVENTARIO",
        bg="blue",
        fg="white",
        font=("Arial", 12, "bold"),
        command=cargar_datos
    ).pack(pady=10)