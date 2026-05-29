import cv2
import cv2.aruco as aruco
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import time

# =========================================
# BASE DE DATOS
# =========================================

conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

# =========================================
# CAMARA
# =========================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Resolucion
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Verificar camara
if not cap.isOpened():
    print("No se pudo abrir la camara")
    exit()

# =========================================
# DICCIONARIO ARUCO
# =========================================

diccionario = aruco.getPredefinedDictionary(
    aruco.DICT_4X4_50
)

# =========================================
# CONTROL DE DETECCIONES
# =========================================

tiempos_detectados = {}

# Tiempo para evitar registros duplicados
cooldown = 3

# =========================================
# INTERFAZ
# =========================================

ventana = tk.Tk()

ventana.title("Sistema Farmaceutico ArUco")

ventana.geometry("1200x700")

ventana.configure(bg="#EAEAEA")

# =========================================
# FRAME SUPERIOR
# =========================================

frame_superior = tk.Frame(
    ventana,
    bg="#EAEAEA"
)

frame_superior.pack(
    fill="both",
    expand=True
)

# =========================================
# CAMARA
# =========================================

label_camara = tk.Label(
    frame_superior,
    bg="black"
)

label_camara.pack(
    side="left",
    padx=10,
    pady=10
)

# =========================================
# PANEL INFORMACION
# =========================================

frame_info = tk.Frame(
    frame_superior,
    bg="white",
    bd=2,
    relief="solid"
)

frame_info.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================================
# TITULO
# =========================================

titulo = tk.Label(
    frame_info,
    text="INFORMACION DEL MEDICAMENTO",
    font=("Arial", 18, "bold"),
    bg="white"
)

titulo.pack(pady=20)

# =========================================
# VARIABLES VISUALES
# =========================================

texto_id = tk.StringVar()
texto_nombre = tk.StringVar()
texto_dosis = tk.StringVar()
texto_lote = tk.StringVar()
texto_caducidad = tk.StringVar()
texto_fabricante = tk.StringVar()
texto_stock = tk.StringVar()

# =========================================
# LABELS
# =========================================

labels = [
    ("ID:", texto_id),
    ("Nombre:", texto_nombre),
    ("Dosis:", texto_dosis),
    ("Lote:", texto_lote),
    ("Caducidad:", texto_caducidad),
    ("Fabricante:", texto_fabricante),
    ("Stock:", texto_stock)
]

for texto, variable in labels:

    fila = tk.Frame(
        frame_info,
        bg="white"
    )

    fila.pack(
        anchor="w",
        pady=8,
        padx=20
    )

    tk.Label(
        fila,
        text=texto,
        font=("Arial", 14, "bold"),
        bg="white"
    ).pack(side="left")

    tk.Label(
        fila,
        textvariable=variable,
        font=("Arial", 14),
        bg="white"
    ).pack(side="left")

# =========================================
# HISTORIAL
# =========================================

frame_historial = tk.Frame(
    ventana,
    bg="white",
    bd=2,
    relief="solid"
)

frame_historial.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

tk.Label(
    frame_historial,
    text="HISTORIAL DE ESCANEOS",
    font=("Arial", 16, "bold"),
    bg="white"
).pack(pady=10)

lista_historial = tk.Listbox(
    frame_historial,
    font=("Arial", 12),
    height=10
)

lista_historial.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================================
# FUNCION VIDEO
# =========================================

def actualizar_video():

    ret, frame = cap.read()

    if ret:

        # Detectar ArUcos
        corners, ids, rejected = aruco.detectMarkers(
            frame,
            diccionario
        )

        if ids is not None:

            # Dibujar ArUcos
            aruco.drawDetectedMarkers(
                frame,
                corners,
                ids
            )

            for id in ids:

                id_detectado = int(id[0])

                tiempo_actual = time.time()

                # Evitar multiples lecturas
                if (
                    id_detectado not in tiempos_detectados
                    or
                    tiempo_actual - tiempos_detectados[id_detectado] > cooldown
                ):

                    # Guardar tiempo
                    tiempos_detectados[id_detectado] = tiempo_actual

                    # Buscar producto
                    cursor.execute(
                        "SELECT * FROM productos WHERE id=?",
                        (id_detectado,)
                    )

                    producto = cursor.fetchone()

                    if producto:

                        nombre = producto[1]
                        dosis = producto[2]
                        lote = producto[3]
                        caducidad = producto[4]
                        fabricante = producto[5]
                        stock = producto[6]

                        # Aumentar stock
                        nuevo_stock = stock + 1

                        cursor.execute(
                            """
                            UPDATE productos
                            SET stock=?
                            WHERE id=?
                            """,
                            (nuevo_stock, id_detectado)
                        )

                        conexion.commit()

                        stock = nuevo_stock

                        # Actualizar interfaz
                        texto_id.set(id_detectado)
                        texto_nombre.set(nombre)
                        texto_dosis.set(dosis)
                        texto_lote.set(lote)
                        texto_caducidad.set(caducidad)
                        texto_fabricante.set(fabricante)
                        texto_stock.set(stock)

                        # Historial
                        lista_historial.insert(
                            0,
                            f"ID {id_detectado} | "
                            f"{nombre} | "
                            f"Stock: {stock}"
                        )

                        # Limitar historial
                        if lista_historial.size() > 20:
                            lista_historial.delete(20)

        # =========================================
        # MOSTRAR VIDEO EN TKINTER
        # =========================================

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        imagen = Image.fromarray(frame_rgb)

        imagen = imagen.resize((500, 400))

        imagen_tk = ImageTk.PhotoImage(imagen)

        label_camara.imgtk = imagen_tk

        label_camara.configure(
            image=imagen_tk
        )

    ventana.after(
        10,
        actualizar_video
    )

# =========================================
# CERRAR
# =========================================

def cerrar():

    cap.release()

    conexion.close()

    ventana.destroy()

ventana.protocol(
    "WM_DELETE_WINDOW",
    cerrar
)

# =========================================
# INICIAR
# =========================================

actualizar_video()

ventana.mainloop()