import pyodbc

def conectar_bd_alimentos():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NCHRAMO1\\SQLEXPRESS;'
            'DATABASE=AgenteResiduosDB;'  # Misma BD, nuevas tablas
            'Trusted_Connection=yes;'
        )
        return conexion
    except Exception as e:
        print("Error al conectar con BD de alimentos:", e)
        return None

def insertar_alimento(cursor, nombre, propiedad, categoria, observacion):
    try:
        query = "INSERT INTO alimentos (nombre, propiedad, categoria, observaciones) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nombre, propiedad, categoria, observacion))
    except Exception as e:
        print("Error al insertar alimento:", e)

def guardar_regla_alimentos(cursor, palabra_clave, propiedad, categoria, observacion):
    try:
        query = "INSERT INTO reglas_alimentos (palabra_clave, propiedad, categoria, observaciones) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (palabra_clave, propiedad, categoria, observacion))
    except Exception as e:
        print("Error al guardar la regla de alimento:", e)

def obtener_reglas_alimentos(cursor):
    try:
        query = "SELECT palabra_clave, propiedad, categoria FROM reglas_alimentos"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener reglas de alimentos:", e)
        return []
