import sqlite3

conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

medicamentos = [

    (1, "Paracetamol", "500mg", "LOT-1023", "2027-05-14", "Pfizer", 0),

    (2, "Ibuprofeno", "400mg", "LOT-2045", "2026-11-20", "Bayer", 0),

    (3, "Amoxicilina", "250mg", "LOT-3301", "2027-01-08", "MK", 0),

    (4, "Omeprazol", "20mg", "LOT-4120", "2028-03-15", "Sandoz", 0),

    (5, "Loratadina", "10mg", "LOT-5509", "2026-08-02", "Genomma Lab", 0),

    (6, "Aspirina", "100mg", "LOT-6022", "2027-09-11", "Bayer", 0),

    (7, "Metformina", "850mg", "LOT-7125", "2028-01-25", "Novartis", 0),

    (8, "Losartan", "50mg", "LOT-8450", "2027-12-30", "Pfizer", 0),

    (9, "Diclofenaco", "50mg", "LOT-9018", "2026-10-19", "MK", 0),

    (10, "Azitromicina", "500mg", "LOT-1007", "2027-07-07", "Sandoz", 0)

]

cursor.executemany(
    """
    INSERT OR REPLACE INTO productos
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    medicamentos
)

conexion.commit()
conexion.close()

print("Medicamentos agregados")