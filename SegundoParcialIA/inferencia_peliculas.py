from difflib import SequenceMatcher
from bd_peliculas import obtener_reglas_peliculas
def inferir_pelicula(palabra, cursor):
    palabra = palabra.lower()
    query = "SELECT genero, sinopsis FROM peliculas WHERE nombre LIKE ?"
    cursor.execute(query, (f"%{palabra}%",))
    resultado = cursor.fetchone()
    if resultado:
        return resultado.genero, resultado.sinopsis
    reglas = obtener_reglas_peliculas(cursor)
    for regla in reglas:
        if palabra == regla.palabra_clave.lower():
            return regla.genero, regla.sinopsis
    return None, None
def aplicar_inferencia_peliculas(premisa_condicional, segunda_premisa):
    if "si" in premisa_condicional and "entonces" in premisa_condicional:
        partes = premisa_condicional.lower().split("entonces")
        antecedente = partes[0].replace("si", "").strip()
        consecuente = partes[1].strip()
        hecho = segunda_premisa.lower().strip()
        if SequenceMatcher(None, antecedente, hecho).ratio() > 0.85:
            return f"Por Modus Ponens (película), se concluye que: {consecuente}"
        elif SequenceMatcher(None, f"no {consecuente}", hecho).ratio() > 0.85:
            if " es " in antecedente:
                sujeto, atributo = antecedente.split(" es ", 1)
                return f"Por Modus Tollens (película), se concluye que: {sujeto.strip()} no es {atributo.strip()}"
            return f"Por Modus Tollens (película), se concluye que: no {antecedente}"

    return "No se pudo aplicar inferencia sobre películas."
