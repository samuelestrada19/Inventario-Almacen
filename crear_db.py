import sqlite3

conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    dosis TEXT,
    lote TEXT,
    caducidad TEXT,
    fabricante TEXT,
    stock INTEGER
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada")