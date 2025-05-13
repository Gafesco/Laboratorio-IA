from difflib import SequenceMatcher
def inferir_alimento(palabra, cursor):
    palabra = palabra.lower()

    query = "SELECT propiedad, categoria FROM alimentos WHERE nombre LIKE ?"
    cursor.execute(query, (f"%{palabra}%",))
    resultado = cursor.fetchone()
    if resultado:
        return resultado.propiedad, resultado.categoria
    return None, None
def aplicar_inferencia_alimentos(premisa_condicional, segunda_premisa):
    if "si" in premisa_condicional and "entonces" in premisa_condicional:
        partes = premisa_condicional.lower().split("entonces")
        antecedente = partes[0].replace("si", "").strip()
        consecuente = partes[1].strip()
        hecho = segunda_premisa.lower().strip()
        if SequenceMatcher(None, antecedente, hecho).ratio() > 0.85:
            return f"Por Modus Ponens (alimento), se concluye que: {consecuente}"
        elif SequenceMatcher(None, f"no {consecuente}", hecho).ratio() > 0.85:
            if " es " in antecedente:
                sujeto, atributo = antecedente.split(" es ", 1)
                return f"Por Modus Tollens (alimento), se concluye que: {sujeto.strip()} no es {atributo.strip()}"
            elif " tiene " in antecedente:
                sujeto, atributo = antecedente.split(" tiene ", 1)
                return f"Por Modus Tollens (alimento), se concluye que: {sujeto.strip()} no tiene {atributo.strip()}"
            else:
                return f"Por Modus Tollens (alimento), se concluye que: no {antecedente}"

    return "No se pudo aplicar inferencia sobre alimentos."
