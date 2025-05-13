import spacy

nlp = spacy.load("es_core_news_sm")

def extraer_residuo(frase_usuario):
    doc = nlp(frase_usuario)
    palabras_clave = []

    for token in doc:

        if token.pos_ in ("NOUN", "PROPN"):
            palabras_clave.append(token.text.lower())

    return palabras_clave


from bd import conectar_bd
from bd_alimentos import conectar_bd_alimentos
from bd_peliculas import conectar_bd_peliculas

def detectar_tema(frase):
    frase = frase.lower()
    palabras = frase.split()

    palabras_residuos = [
        "residuo", "reciclable", "reciclar", "basura", "contenedor", "desecho",
        "botella", "papel", "cartón", "vidrio", "orgánico", "plástico", "tapita", "lata"
    ]

    palabras_alimentos = [
        "alimento", "comida", "fruta", "saludable", "grasoso", "azúcar", "dieta",
        "carne", "vegetal", "ensalada", "frito", "pan", "bebida", "comestible"
    ]

    palabras_peliculas = [
        "pelicula", "películas", "cine", "género", "director", "trama", "animación", "acción", "terror", "comedia",
        "sinopsis"
    ]

    if any(p in frase for p in palabras_residuos):
        return "residuos"
    elif any(p in frase for p in palabras_alimentos):
        return "alimentos"
    elif any(p in frase for p in palabras_peliculas):
        return "peliculas"

    conn_res = conectar_bd()
    if conn_res:
        cur = conn_res.cursor()
        for palabra in palabras:
            cur.execute("SELECT COUNT(*) FROM residuos WHERE nombre LIKE ?", (f"%{palabra}%",))
            if cur.fetchone()[0] > 0:
                conn_res.close()
                return "residuos"
        conn_res.close()

    conn_ali = conectar_bd_alimentos()
    if conn_ali:
        cur = conn_ali.cursor()
        for palabra in palabras:
            cur.execute("SELECT COUNT(*) FROM alimentos WHERE nombre LIKE ?", (f"%{palabra}%",))
            if cur.fetchone()[0] > 0:
                conn_ali.close()
                return "alimentos"
        conn_ali.close()

    conn_pel = conectar_bd_peliculas()
    if conn_pel:
        cur = conn_pel.cursor()
        for palabra in palabras:
            cur.execute("SELECT COUNT(*) FROM peliculas WHERE nombre LIKE ?", (f"%{palabra}%",))
            if cur.fetchone()[0] > 0:
                conn_pel.close()
                return "peliculas"
        conn_pel.close()

    return "desconocido"
