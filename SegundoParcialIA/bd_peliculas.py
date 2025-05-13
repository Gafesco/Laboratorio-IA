import pyodbc

def conectar_bd_peliculas():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-NCHRAMO1\\SQLEXPRESS;'
            'DATABASE=AgenteResiduosDB;'
            'Trusted_Connection=yes;'
        )
        return conexion
    except Exception as e:
        print("Error al conectar con BD de películas:", e)
        return None

def insertar_pelicula(cursor, nombre, genero, sinopsis):
    try:
        query = "INSERT INTO peliculas (nombre, genero, sinopsis) VALUES (?, ?, ?)"
        cursor.execute(query, (nombre, genero, sinopsis))
    except Exception as e:
        print("Error al insertar película:", e)

def guardar_regla_peliculas(cursor, palabra_clave, genero, sinopsis):
    try:
        query = "INSERT INTO reglas_peliculas (palabra_clave, genero, sinopsis) VALUES (?, ?, ?)"
        cursor.execute(query, (palabra_clave, genero, sinopsis))
    except Exception as e:
        print("Error al guardar la regla de película:", e)

def obtener_reglas_peliculas(cursor):
    try:
        query = "SELECT palabra_clave, genero, sinopsis FROM reglas_peliculas"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener reglas de películas:", e)
        return []
