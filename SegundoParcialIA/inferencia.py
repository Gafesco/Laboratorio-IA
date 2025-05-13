from bd import obtener_reglas
from difflib import SequenceMatcher

contenedores = {
    "reciclable": "blanco",
    "orgánico": "verde",
    "no reciclable": "negro",
    "vidrio": "rojo"
}

palabras_residuos = [
    "orgánico", "reciclable", "no reciclable", "vidrio",
    "verde", "blanco", "negro", "rojo",
    "residuo", "residuos", "desecho", "contenedor", "basura",
    "pilas", "botella", "frasco", "plástico", "papel", "abono", "compost", "restos", "envase"
]

def inferir_residuo(palabra, cursor):
    palabra = palabra.lower()
    reglas = obtener_reglas(cursor)
    for regla in reglas:
        if palabra == regla.palabra_clave.lower():
            return regla.tipo, regla.contenedor
    return None, None

def aplicar_modus_ponens(premisa_condicional, premisa_hecho):
    if "si" in premisa_condicional and "entonces" in premisa_condicional:
        partes = premisa_condicional.lower().split("entonces")
        antecedente = partes[0].replace("si", "").strip()
        consecuente = partes[1].strip()
        hecho = premisa_hecho.lower().strip()

        if SequenceMatcher(None, antecedente, hecho).ratio() > 0.85:
            return f"Por Modus Ponens, se concluye que: {consecuente}"
    return "No se puede aplicar Modus Ponens."

def aplicar_modus_tollens(premisa_condicional, negacion_consecuente):
    if "si" in premisa_condicional and "entonces" in premisa_condicional:
        partes = premisa_condicional.lower().split("entonces")
        antecedente = partes[0].replace("si", "").strip()
        consecuente = partes[1].strip()
        negado = negacion_consecuente.lower().strip()

        if SequenceMatcher(None, f"no {consecuente}", negado).ratio() > 0.85:
            if " es " in antecedente:
                sujeto, atributo = [p.strip() for p in antecedente.split(" es ", 1)]
                sujeto = limpiar_errores_comunes(sujeto)
                atributo = limpiar_errores_comunes(atributo)
                return f"Por Modus Tollens, se concluye que: {sujeto} no es {atributo}"
            return f"Por Modus Tollens, se concluye que: no {antecedente}"
    return "No se puede aplicar Modus Tollens."


def detectar_regla_y_aplicar(premisa_condicional, segunda_premisa):
    texto_completo = f"{premisa_condicional.lower()} {segunda_premisa.lower()}"

    if not any(palabra in texto_completo for palabra in palabras_residuos):
        return "No se reconoce como una regla para los temas del sistema. No se puede aplicar inferencia."

    if "si" in premisa_condicional and "entonces" in premisa_condicional:
        partes = premisa_condicional.lower().split("entonces")
        antecedente = partes[0].replace("si", "").strip()
        consecuente = partes[1].strip()
        segunda = segunda_premisa.lower().strip()

        if SequenceMatcher(None, antecedente, segunda).ratio() > 0.85:
            return aplicar_modus_ponens(premisa_condicional, segunda_premisa)

        elif SequenceMatcher(None, f"no {consecuente}", segunda).ratio() > 0.85:
            return aplicar_modus_tollens(premisa_condicional, segunda_premisa)

        else:
            return "No se pudo aplicar ninguna regla. Asegúrate de que la segunda premisa sea válida."
    else:
        return "No parece una oración condicional válida (falta 'si' o 'entonces')."

def verificar_residuo_sucio(oracion):
    oracion = oracion.lower()
    if "sucio" in oracion or "sucia" in oracion:
        if "reciclable" in oracion or "reciclar" in oracion:
            return "Atención: Si el residuo está sucio, entonces no se puede reciclar."
    return None
def limpiar_errores_comunes(texto):
    correcciones = {
        "reduo": "residuo",
        "reciduo": "residuo",
        "resido": "residuo",
        "recepiente": "recipiente",
    }
    for error, correccion in correcciones.items():
        texto = texto.replace(error, correccion)
    return texto
