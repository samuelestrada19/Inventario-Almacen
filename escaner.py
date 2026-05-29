import cv2
import cv2.aruco as aruco
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import time

def crear_frame_escaner(frame_principal):

    # =========================================
    # BASE DE DATOS
    # =========================================

    conexion = sqlite3.connect("productos.db")
    cursor = conexion.cursor()

    # =========================================
    # CAMARA
    # =========================================

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():

        tk.Label(
            frame_principal,
            text="No se pudo abrir la camara",
            font=("Arial", 20)
        ).pack()

        return

    # =========================================
    # ARUCO
    # =========================================

    diccionario = aruco.getPredefinedDictionary(
        aruco.DICT_4X4_50
    )

    tiempos_detectados = {}

    cooldown = 3

    # =========================================
    # FRAMES
    # =========================================

    frame_superior = tk.Frame(frame_principal)

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

    tk.Label(
        frame_info,
        text="INFORMACION DEL MEDICAMENTO",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=20)

    # =========================================
    # VARIABLES
    # =========================================

    texto_id = tk.StringVar()
    texto_nombre = tk.StringVar()
    texto_dosis = tk.StringVar()
    texto_lote = tk.StringVar()
    texto_caducidad = tk.StringVar()
    texto_fabricante = tk.StringVar()
    texto_stock = tk.StringVar()

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
        frame_principal,
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
    # VIDEO
    # =========================================

    def actualizar_video():

        ret, frame = cap.read()

        if ret:

            corners, ids, rejected = aruco.detectMarkers(
                frame,
                diccionario
            )

            if ids is not None:

                aruco.drawDetectedMarkers(
                    frame,
                    corners,
                    ids
                )

                for id in ids:

                    id_detectado = int(id[0])

                    tiempo_actual = time.time()

                    if (
                        id_detectado not in tiempos_detectados
                        or
                        tiempo_actual - tiempos_detectados[id_detectado] > cooldown
                    ):

                        tiempos_detectados[id_detectado] = tiempo_actual

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

                            texto_id.set(id_detectado)
                            texto_nombre.set(nombre)
                            texto_dosis.set(dosis)
                            texto_lote.set(lote)
                            texto_caducidad.set(caducidad)
                            texto_fabricante.set(fabricante)
                            texto_stock.set(stock)

                            lista_historial.insert(
                                0,
                                f"{nombre} | Stock: {stock}"
                            )

                            if lista_historial.size() > 20:
                                lista_historial.delete(20)

            # Mostrar video
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

        frame_principal.after(
            10,
            actualizar_video
        )

    actualizar_video()