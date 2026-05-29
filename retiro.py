import tkinter as tk
from tkinter import ttk
import sqlite3

def crear_frame_retiro(frame):

    conexion = sqlite3.connect("productos.db")

    cursor = conexion.cursor()

    # =====================================
    # TITULO
    # =====================================

    tk.Label(
        frame,
        text="RETIRO DE MEDICAMENTOS",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # =====================================
    # TABLA
    # =====================================

    columnas = (
        "Nombre",
        "Dosis",
        "Stock"
    )

    tabla = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings",
        height=15
    )

    for col in columnas:

        tabla.heading(col, text=col)

        tabla.column(
            col,
            width=200
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

        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)

        # Leer DB
        cursor.execute(
            "SELECT * FROM productos"
        )

        productos = cursor.fetchall()

        # Insertar datos
        for producto in productos:

            tabla.insert(
                "",
                "end",
                values=(
                    producto[1],  # nombre
                    producto[2],  # dosis
                    producto[6]   # stock
                )
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

    # =====================================
    # FRAME RETIRO
    # =====================================

    frame_retirar = tk.Frame(frame)

    frame_retirar.pack(pady=10)

    # =====================================
    # CANTIDAD
    # =====================================

    tk.Label(
        frame_retirar,
        text="Cantidad:",
        font=("Arial", 12)
    ).pack(side="left")

    entrada_cantidad = tk.Entry(
        frame_retirar,
        width=10,
        font=("Arial", 12)
    )

    entrada_cantidad.pack(
        side="left",
        padx=10
    )

    # =====================================
    # RETIRAR PRODUCTO
    # =====================================

    def retirar_producto():

        seleccionado = tabla.selection()

        if not seleccionado:
            return

        cantidad = entrada_cantidad.get()

        if not cantidad.isdigit():
            return

        cantidad = int(cantidad)

        # Datos seleccionados
        datos = tabla.item(
            seleccionado[0]
        )["values"]

        nombre_producto = datos[0]

        stock_actual = datos[2]

        # Buscar ID usando nombre
        cursor.execute(
            "SELECT id FROM productos WHERE nombre=?",
            (nombre_producto,)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            return

        id_producto = resultado[0]

        # Nuevo stock
        nuevo_stock = stock_actual - cantidad

        if nuevo_stock < 0:
            nuevo_stock = 0

        # Actualizar DB
        cursor.execute(
            """
            UPDATE productos
            SET stock=?
            WHERE id=?
            """,
            (nuevo_stock, id_producto)
        )

        conexion.commit()

        # Recargar tabla
        cargar_datos()

        # Limpiar entrada
        entrada_cantidad.delete(0, tk.END)

    # =====================================
    # BOTON RETIRAR
    # =====================================

    tk.Button(
        frame_retirar,
        text="RETIRAR",
        bg="red",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        command=retirar_producto
    ).pack(side="left")