import pyodbc
def conectar_bd():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NCHRAMO1\\SQLEXPRESS;'
            'DATABASE=AgenteResiduosDB;'
            'Trusted_Connection=yes;'
        )
        return conexion
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return None

def insertar_residuo(cursor, nombre, tipo, contenedor, observacion):
    try:
        query = "INSERT INTO residuos (nombre, tipo, contenedor, observaciones) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nombre, tipo, contenedor, observacion))
        print(f"Residuo '{nombre}' agregado correctamente.\n")
    except Exception as e:
        print("Error al insertar el residuo:", e)

def guardar_regla(cursor, palabra_clave, tipo, contenedor, observacion):
    try:
        query = "INSERT INTO reglas (palabra_clave, tipo, contenedor, observaciones) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (palabra_clave, tipo, contenedor, observacion))
        print(f"Regla para '{palabra_clave}' agregada correctamente.")
    except Exception as e:
        print("Error al guardar la regla:", e)

def obtener_reglas(cursor):
    try:
        query = "SELECT palabra_clave, tipo, contenedor FROM reglas"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener las reglas:", e)
        return []
