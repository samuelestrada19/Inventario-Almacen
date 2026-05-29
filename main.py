import tkinter as tk
from tkinter import ttk

from escaner import crear_frame_escaner
from retiro import crear_frame_retiro
from inventario import crear_frame_inventario

# =====================================
# VENTANA PRINCIPAL
# =====================================

ventana = tk.Tk()

ventana.title("Sistema Farmaceutico ArUco")

ventana.geometry("1400x800")

# =====================================
# NOTEBOOK (PESTAÑAS)
# =====================================

tabs = ttk.Notebook(ventana)

tabs.pack(
    fill="both",
    expand=True
)

# =====================================
# CREAR FRAMES
# =====================================

frame_escaner = tk.Frame(tabs)
frame_retiro = tk.Frame(tabs)
frame_inventario = tk.Frame(tabs)

# =====================================
# AGREGAR PESTAÑAS
# =====================================

tabs.add(
    frame_escaner,
    text="Escaner"
)

tabs.add(
    frame_retiro,
    text="Retiro"
)

tabs.add(
    frame_inventario,
    text="Inventario"
)

# =====================================
# CARGAR INTERFACES
# =====================================

crear_frame_escaner(frame_escaner)

crear_frame_retiro(frame_retiro)

crear_frame_inventario(frame_inventario)

# =====================================
# INICIAR
# =====================================

ventana.mainloop()