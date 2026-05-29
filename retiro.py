import tkinter as tk
from tkinter import ttk
import sqlite3

def crear_frame_retiro(frame):

    conexion = sqlite3.connect("productos.db")

    cursor = conexion.cursor()

    pedido = []

    # =====================================
    # TITULO
    # =====================================

    tk.Label(
        frame,
        text="RETIRO DE MEDICAMENTOS",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    # =====================================
    # FRAME SUPERIOR
    # =====================================

    frame_superior = tk.Frame(frame)

    frame_superior.pack(fill="both", expand=True)

    # =====================================
    # INVENTARIO
    # =====================================

    frame_inventario = tk.Frame(frame_superior)

    frame_inventario.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10
    )

    tk.Label(
        frame_inventario,
        text="INVENTARIO",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    columnas = (
        "Nombre",
        "Dosis",
        "Stock"
    )

    tabla = ttk.Treeview(
        frame_inventario,
        columns=columnas,
        show="headings",
        height=15
    )

    for col in columnas:

        tabla.heading(col, text=col)

        tabla.column(col, width=150)

    tabla.pack(fill="both", expand=True)

    # =====================================
    # PEDIDO
    # =====================================

    frame_pedido = tk.Frame(frame_superior)

    frame_pedido.pack(
        side="right",
        fill="both",
        expand=True,
        padx=10
    )

    tk.Label(
        frame_pedido,
        text="PEDIDO",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    tabla_pedido = ttk.Treeview(
        frame_pedido,
        columns=("Nombre", "Cantidad"),
        show="headings",
        height=15
    )

    tabla_pedido.heading("Nombre", text="Nombre")
    tabla_pedido.heading("Cantidad", text="Cantidad")

    tabla_pedido.column("Nombre", width=180)
    tabla_pedido.column("Cantidad", width=100)

    tabla_pedido.pack(fill="both", expand=True)

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
                values=(
                    producto[1],
                    producto[2],
                    producto[6]
                )
            )

    cargar_datos()

    # =====================================
    # CONTROLES
    # =====================================

    frame_controles = tk.Frame(frame)

    frame_controles.pack(pady=20)

    tk.Label(
        frame_controles,
        text="Cantidad:"
    ).pack(side="left")

    entrada_cantidad = tk.Entry(
        frame_controles,
        width=10
    )

    entrada_cantidad.pack(
        side="left",
        padx=10
    )

    # =====================================
    # AGREGAR AL PEDIDO
    # =====================================

    def agregar_pedido():

        seleccionado = tabla.selection()

        if not seleccionado:
            return

        cantidad = entrada_cantidad.get()

        if not cantidad.isdigit():
            return

        cantidad = int(cantidad)

        datos = tabla.item(
            seleccionado[0]
        )["values"]

        nombre = datos[0]

        pedido.append(
            (nombre, cantidad)
        )

        tabla_pedido.insert(
            "",
            "end",
            values=(
                nombre,
                cantidad
            )
        )

        entrada_cantidad.delete(0, tk.END)

    # =====================================
    # CONFIRMAR RETIRO
    # =====================================

    def confirmar_retiro():

        for nombre, cantidad in pedido:

            cursor.execute(
                """
                SELECT id, stock
                FROM productos
                WHERE nombre=?
                """,
                (nombre,)
            )

            resultado = cursor.fetchone()

            if resultado:

                id_producto = resultado[0]

                stock_actual = resultado[1]

                nuevo_stock = stock_actual - cantidad

                if nuevo_stock < 0:
                    nuevo_stock = 0

                cursor.execute(
                    """
                    UPDATE productos
                    SET stock=?
                    WHERE id=?
                    """,
                    (
                        nuevo_stock,
                        id_producto
                    )
                )

        conexion.commit()

        pedido.clear()

        for fila in tabla_pedido.get_children():
            tabla_pedido.delete(fila)

        cargar_datos()

    # =====================================
    # BOTONES
    # =====================================

    tk.Button(
        frame_controles,
        text="AGREGAR AL PEDIDO",
        bg="orange",
        fg="white",
        font=("Arial", 12, "bold"),
        command=agregar_pedido
    ).pack(side="left", padx=10)

    tk.Button(
        frame_controles,
        text="CONFIRMAR RETIRO",
        bg="red",
        fg="white",
        font=("Arial", 12, "bold"),
        command=confirmar_retiro
    ).pack(side="left", padx=10)

    tk.Button(
        frame_controles,
        text="RECARGAR INVENTARIO",
        bg="blue",
        fg="white",
        font=("Arial", 12, "bold"),
        command=cargar_datos
    ).pack(side="left", padx=10)