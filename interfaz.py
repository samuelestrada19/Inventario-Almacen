import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Conexion DB
conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

# Ventana principal
ventana = tk.Tk()
ventana.title("Inventario Farmaceutico")
ventana.geometry("1200x600")

# =========================
# TABLA INVENTARIO
# =========================

tabla = ttk.Treeview(
    ventana,
    columns=(
        "ID",
        "Nombre",
        "Dosis",
        "Lote",
        "Caducidad",
        "Fabricante",
        "Stock"
    ),
    show="headings",
    height=10
)

columnas = [
    "ID",
    "Nombre",
    "Dosis",
    "Lote",
    "Caducidad",
    "Fabricante",
    "Stock"
]

for col in columnas:
    tabla.heading(col, text=col)

tabla.pack(fill="x", padx=10, pady=10)

# =========================
# FUNCION CARGAR DATOS
# =========================

def cargar_datos():

    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    for producto in productos:
        tabla.insert("", tk.END, values=producto)

# =========================
# FRAME CONTROLES
# =========================

frame_controles = tk.Frame(ventana)
frame_controles.pack(pady=10)

tk.Label(
    frame_controles,
    text="Cantidad:"
).grid(row=0, column=0, padx=5)

entrada_cantidad = tk.Entry(frame_controles, width=10)
entrada_cantidad.grid(row=0, column=1, padx=5)

# =========================
# TABLA PEDIDO
# =========================

tk.Label(
    ventana,
    text="Pedido Actual",
    font=("Arial", 14, "bold")
).pack()

tabla_pedido = ttk.Treeview(
    ventana,
    columns=("ID", "Nombre", "Cantidad"),
    show="headings",
    height=8
)

tabla_pedido.heading("ID", text="ID")
tabla_pedido.heading("Nombre", text="Nombre")
tabla_pedido.heading("Cantidad", text="Cantidad")

tabla_pedido.pack(fill="x", padx=10, pady=10)

# =========================
# LISTA PEDIDO
# =========================

pedido = []

# =========================
# AGREGAR AL PEDIDO
# =========================

def agregar_pedido():

    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning(
            "Error",
            "Selecciona un medicamento"
        )
        return

    try:
        cantidad = int(entrada_cantidad.get())

    except:
        messagebox.showwarning(
            "Error",
            "Cantidad invalida"
        )
        return

    datos = tabla.item(seleccionado)["values"]

    id_producto = datos[0]
    nombre = datos[1]
    stock_actual = datos[6]

    if cantidad <= 0:
        messagebox.showwarning(
            "Error",
            "Cantidad debe ser mayor a 0"
        )
        return

    if cantidad > stock_actual:
        messagebox.showwarning(
            "Error",
            "No hay suficiente stock"
        )
        return

    # Guardar en pedido
    pedido.append((id_producto, nombre, cantidad))

    tabla_pedido.insert(
        "",
        tk.END,
        values=(id_producto, nombre, cantidad)
    )

    entrada_cantidad.delete(0, tk.END)

# =========================
# PROCESAR RETIRO
# =========================

def procesar_retiro():

    if not pedido:
        messagebox.showwarning(
            "Error",
            "No hay productos en el pedido"
        )
        return

    for item in pedido:

        id_producto = item[0]
        cantidad = item[2]

        cursor.execute(
            """
            UPDATE productos
            SET stock = stock - ?
            WHERE id=?
            """,
            (cantidad, id_producto)
        )

    conexion.commit()

    # Limpiar pedido
    pedido.clear()

    for fila in tabla_pedido.get_children():
        tabla_pedido.delete(fila)

    cargar_datos()

    messagebox.showinfo(
        "Exito",
        "Retiro realizado correctamente"
    )

# =========================
# BOTONES
# =========================

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

btn_agregar = tk.Button(
    frame_botones,
    text="Agregar al Pedido",
    font=("Arial", 12),
    command=agregar_pedido
)

btn_agregar.grid(row=0, column=0, padx=10)

btn_retirar = tk.Button(
    frame_botones,
    text="Procesar Retiro",
    font=("Arial", 12),
    bg="red",
    fg="white",
    command=procesar_retiro
)

btn_retirar.grid(row=0, column=1, padx=10)

# =========================
# CARGAR DATOS
# =========================

cargar_datos()

# =========================
# EJECUTAR
# =========================

ventana.mainloop()

# =========================
# CERRAR DB
# =========================

conexion.close()