import cv2
import cv2.aruco as aruco
import sqlite3
import os
import time

# Limpiar terminal
os.system("cls")

# Conexion a la base de datos
conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

# Camara USB
cap = cv2.VideoCapture(1)

# Diccionario ArUco
diccionario = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Control de detecciones
tiempos_detectados = {}

# Tiempo de espera para evitar duplicados
cooldown = 3

# Variables iniciales
nombre = ""
dosis = ""
lote = ""
caducidad = ""
fabricante = ""
stock = 0

# Encabezado de tabla
print("=" * 100)

print(
    f"{'ID':<5}"
    f"{'NOMBRE':<20}"
    f"{'DOSIS':<12}"
    f"{'LOTE':<15}"
    f"{'CADUCIDAD':<15}"
    f"{'FABRICANTE':<20}"
    f"{'STOCK':<10}"
)

print("=" * 100)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error al leer la camara")
        break

    corners, ids, rejected = aruco.detectMarkers(
        frame,
        diccionario
    )

    if ids is not None:

        # Dibujar ArUcos detectados
        aruco.drawDetectedMarkers(frame, corners, ids)

        for id in ids:

            id_detectado = int(id[0])

            # Tiempo actual
            tiempo_actual = time.time()

            # Evitar multiples registros seguidos
            if (
                id_detectado not in tiempos_detectados
                or
                tiempo_actual - tiempos_detectados[id_detectado] > cooldown
            ):

                # Guardar tiempo de deteccion
                tiempos_detectados[id_detectado] = tiempo_actual

                # Buscar producto en DB
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

                    # SUMAR INVENTARIO
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

                    # Actualizar stock local
                    stock = nuevo_stock

                    # Mostrar en terminal
                    print(
                        f"{id_detectado:<5}"
                        f"{nombre:<20}"
                        f"{dosis:<12}"
                        f"{lote:<15}"
                        f"{caducidad:<15}"
                        f"{fabricante:<20}"
                        f"{stock:<10}"
                    )

            # Mostrar informacion en pantalla
            cv2.putText(
                frame,
                f"ID: {id_detectado}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"{nombre} {dosis}",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Lote: {lote}",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Caducidad: {caducidad}",
                (10, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Fabricante: {fabricante}",
                (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Stock: {stock}",
                (10, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2
            )

    cv2.imshow(
        "Inventario Farmaceutico ArUco",
        frame
    )

    # ESC para salir
    tecla = cv2.waitKey(1)

    if tecla == 27:
        break

# Liberar recursos
cap.release()
conexion.close()
cv2.destroyAllWindows()