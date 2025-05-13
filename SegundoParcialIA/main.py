from bd import conectar_bd, insertar_residuo, guardar_regla
from bd_alimentos import conectar_bd_alimentos
from bd_peliculas import conectar_bd_peliculas
from pln import extraer_residuo, detectar_tema
from inferencia import inferir_residuo, detectar_regla_y_aplicar, verificar_residuo_sucio
from Inferencia_alimentos import inferir_alimento, aplicar_inferencia_alimentos
from inferencia_peliculas import inferir_pelicula, aplicar_inferencia_peliculas

contenedores = {
    "reciclable": "blanco",
    "no reciclable": "negro",
    "orgánico": "verde",
    "vidrio": "rojo"
}

print("Bienvenido al agente inteligente.")
print("Puedes hablar sobre residuos, alimentos o películas. Escribe 'salir' para terminar.\n")

while True:
    frase = input("Tú: ")

    if frase.strip().lower() == "salir":
        print("Adiós. ¡Gracias por usar el sistema!")
        break

    tema = detectar_tema(frase)

    if tema == "residuos":
        conn = conectar_bd()
        if not conn:
            print("No se pudo conectar a la base de residuos.")
            continue
        cursor = conn.cursor()

        if frase.lower().startswith("si") and "entonces" in frase.lower():
            print("\nParece que ingresaste una regla lógica condicional sobre residuos.")
            segunda_premisa = input("Escribe la segunda premisa: ")
            resultado = detectar_regla_y_aplicar(frase, segunda_premisa)
            print(resultado + "\n")
            conn.close()
            continue

        advertencia = verificar_residuo_sucio(frase)
        if advertencia:
            print(advertencia)
            conn.close()
            continue

        residuos_detectados = extraer_residuo(frase)
        if residuos_detectados:
            encontrado = False
            for palabra in residuos_detectados:
                query = "SELECT nombre, tipo, contenedor, observaciones FROM residuos WHERE nombre LIKE ?"
                cursor.execute(query, (f"%{palabra}%",))
                fila = cursor.fetchone()
                if fila:
                    print(f"\nClasificación para: {fila.nombre}")
                    print(f"Tipo: {fila.tipo}")
                    print(f"Contenedor: {fila.contenedor}")
                    print(f"Observación: {fila.observaciones}\n")
                    encontrado = True
                    break

            if not encontrado:
                for palabra in residuos_detectados:
                    tipo, contenedor = inferir_residuo(palabra, cursor)
                    if tipo and contenedor:
                        print(f"\nPor inferencia, '{palabra}' es de tipo '{tipo}'")
                        print(f"Va en el contenedor: {contenedor}\n")
                        encontrado = True
                        break

                if not encontrado:
                    print("No se encontró ese residuo ni se pudo inferir.")
                    respuesta = input("¿Deseas agregar este residuo al sistema? (si/no): ").strip().lower()
                    if respuesta == "si":
                        nombre = input("Ingresa el nombre del residuo: ").strip()
                        tipos_validos = ["reciclable", "no reciclable", "orgánico", "vidrio"]
                        while True:
                            tipo = input("Ingresa el tipo (reciclable, no reciclable, orgánico, vidrio): ").strip().lower()
                            if tipo in tipos_validos:
                                break
                            else:
                                print("Tipo no válido. Intenta de nuevo.")

                        contenedor = contenedores[tipo]
                        observacion = input("Ingresa una observación: ").strip()
                        texto_completo = f"{nombre} {tipo} {observacion}"
                        advertencia_final = verificar_residuo_sucio(texto_completo)
                        if advertencia_final:
                            print(advertencia_final)
                            confirmacion = input("¿Deseas guardar este residuo de todos modos? (si/no): ").strip().lower()
                            if confirmacion != "si":
                                print("Residuo cancelado.\n")
                                conn.close()
                                continue

                        insertar_residuo(cursor, nombre, tipo, contenedor, observacion)
                        guardar_regla(cursor, nombre, tipo, contenedor, observacion)
                        conn.commit()
                        print("Ahora el sistema recordará este residuo en el futuro.\n")
        else:
            print("No detecté ningún residuo en tu frase.\n")
        conn.close()

    elif tema == "alimentos":
        conn_alim = conectar_bd_alimentos()
        if not conn_alim:
            print("No se pudo conectar a la base de alimentos.")
            continue
        cursor_alim = conn_alim.cursor()

        if frase.lower().startswith("si") and "entonces" in frase.lower():
            print("\nParece que ingresaste una regla lógica condicional sobre alimentos.")
            segunda_premisa = input("Escribe la segunda premisa: ")
            resultado = aplicar_inferencia_alimentos(frase, segunda_premisa)
            print(resultado + "\n")
            conn_alim.close()
            continue

        alimentos_detectados = extraer_residuo(frase)
        if not alimentos_detectados:
            print("No detecté ningún alimento en tu frase.\n")
            conn_alim.close()
            continue

        encontrado = False
        for palabra in alimentos_detectados:
            query = "SELECT nombre, propiedad, categoria, observaciones FROM alimentos WHERE nombre LIKE ?"
            cursor_alim.execute(query, (f"%{palabra}%",))
            fila = cursor_alim.fetchone()
            if fila:
                print(f"\nClasificación para: {fila.nombre}")
                print(f"Propiedad: {fila.propiedad}")
                print(f"Categoría: {fila.categoria}")
                print(f"Observación: {fila.observaciones}\n")
                encontrado = True
                break

        if not encontrado:
            for palabra in alimentos_detectados:
                propiedad, categoria = inferir_alimento(palabra, cursor_alim)
                if propiedad and categoria:
                    print(f"\nPor inferencia, '{palabra}' tiene propiedad '{propiedad}'")
                    print(f"Categoría: {categoria}\n")
                    encontrado = True
                    break

        if not encontrado:
            print("No se encontró ese alimento ni se pudo inferir.\n")
        conn_alim.close()

    elif tema == "peliculas":
        conn_pel = conectar_bd_peliculas()
        if not conn_pel:
            print("No se pudo conectar a la base de películas.")
            continue
        cursor_pel = conn_pel.cursor()

        if frase.lower().startswith("si") and "entonces" in frase.lower():
            print("\nParece que ingresaste una regla lógica condicional sobre películas.")
            segunda_premisa = input("Escribe la segunda premisa: ")
            resultado = aplicar_inferencia_peliculas(frase, segunda_premisa)
            print(resultado + "\n")
            conn_pel.close()
            continue

        peliculas_detectadas = extraer_residuo(frase)
        encontrado = False
        for palabra in peliculas_detectadas:
            query = "SELECT nombre, genero, sinopsis FROM peliculas WHERE nombre LIKE ?"
            cursor_pel.execute(query, (f"%{palabra}%",))
            fila = cursor_pel.fetchone()
            if fila:
                print(f"\nClasificación para: {fila.nombre}")
                print(f"Género: {fila.genero}")
                print(f"Sinopsis: {fila.sinopsis}\n")
                encontrado = True
                break

        if not encontrado:
            for palabra in peliculas_detectadas:
                genero, sinopsis = inferir_pelicula(palabra, cursor_pel)
                if genero and sinopsis:
                    print(f"\nPor inferencia, '{palabra}' tiene género '{genero}'")
                    print(f"Sinopsis: {sinopsis}\n")
                    encontrado = True
                    break

        if not encontrado:
            print("No se encontró esa película ni se pudo inferir.\n")
        conn_pel.close()

    else:
        print("No reconozco el tema. Intenta hablar sobre residuos, alimentos o películas.\n")
