"""Programa comprobación boletos en sorteos nacionales"""
# Set-ExecutionPolicy Unrestricted -Scope Process
# venv/Scripts/activate
from primitiva_request import Primitiva
import datetime
sorteo = ""  # única variable global necesaria para el programa

# FUNCIÓN PRIMITIVA########################################################################


def boleto_jugado():
    """
    Se genera un ticket con los inputs del usuario y devuelve los números y el reintegro
    """
    ticket = []
    for numero in range(1, 7):
        ticket.append(input(f"Introduzca el {numero}º número (01-49): "))
    ticket.append(input("Introduzca el reintegro(0-9): "))
    *numeros, reintegro = ticket
    print(f"""
        Los números introducidos han sido {numeros}, y el reintegro {reintegro}
        """)
    return {"numeros": numeros, "reintegro": reintegro}


def juegos_complementario():
    """
    Se pregunta al usuario si ha jugado número complementario
    """
    complementario = input("""
                  Opcional: ¿ha jugado número complementario?
                  0 -> No
                  1 -> Sí
                  """)
    if complementario == "0":
        print("No ha jugado número complementario")
        return False
    elif complementario == "1":
        print("Sí ha jugado número complementario")
        return True
    else:
        print("El valor introducido no es válido")
        return juegos_complementario()


def is_joker():
    """
    Se pregunta al usuario si ha jugado al minijuego Joker
    """
    joker = input("""
                  Opcional: ¿ha jugado Joker?
                  0 -> No
                  1 -> Sí
                  """)
    if joker == "0":
        print("No ha jugado Joker")
        return False
    elif joker == "1":
        print("Sí ha jugado Joker")
        return True
    else:
        print("El valor introducido no es válido")
        return is_joker()


def juego_joker():
    """"
    En caso de haber jugado joker, se le pide al usuario el código jugado
    """
    joker = is_joker()
    joker_ticket = []
    if joker is True:
        joker_ticket = input("Introduzca su código Joker")
        joker_ticket = list(joker_ticket)
        print(f"El código de Joker introducido es {joker_ticket}")
    return joker, joker_ticket


def premiados():
    """
    Con esta función le pedimos al usuario que introduzca una fecha de sorteo y, en base a ésta
    realizaríamos la llamada a la API para obtener la combinación ganadora y también las posibles 
    ganancias para cada combinación
    """
    joker, joker_ticket = juego_joker()
    day = int(input("introduzca el día del sorteo (2 dígitos) "))
    month = int(input("introduzca el mes del sorteo (2 dígitos) "))
    year = int(input("introduzca el año del sorteo (4 dígitos) "))
    fecha = datetime.datetime(year, month, day)
    respuesta = Primitiva.checkWin(fecha)
    premio_bote = int(respuesta[0]["premio_bote"])
    escrutinio = respuesta[0]["escrutinio"]
    # map hace un FOR, pero devuelve valor
    ganancias = list(map(lambda premio: premio["premio"], escrutinio))
    print(f"El bote acumulado para este sorteo es de {premio_bote:,} €")
    combinacion_primi = respuesta[0]["combinacion"]
    combinacion_primi = combinacion_primi.replace(
        "C(", "- ").replace("R(", "- ").replace(")", "")
    premio_primi = combinacion_primi.split(" - ")  # 7 is_comp, 8 reint
    combinacion_joker = respuesta[0]["joker"]["combinacion"]
    joker_primi = list(combinacion_joker)
    *numeros_p, reintegro_p = premio_primi
    print(f"""
          Los números premiados han sido {numeros_p[:6]}, siendo el complementario
          {numeros_p[6]} y el reintegro {reintegro_p}
        """)
    if joker is True:
        print(f"El código de joker premiado es {joker_primi}")

    return {"numeros_p": numeros_p, "reintegro_p": reintegro_p, "joker_primi": joker_primi, "joker_ticket": joker_ticket, "ganancias": ganancias, "joker": joker}


def primitiva():
    """
    Función para comprobar aciertos numéricos y aciertos de Joker
    """
    ticket_jugado = boleto_jugado()
    numeros = ticket_jugado["numeros"]
    reintegro = ticket_jugado["reintegro"]
    is_comp = juegos_complementario()
    resultados_sorteo = premiados()
    numeros_p = resultados_sorteo["numeros_p"]
    reintegro_p = resultados_sorteo["reintegro_p"]
    joker_primi = resultados_sorteo["joker_primi"]
    joker_ticket = resultados_sorteo["joker_ticket"]
    ganancias = resultados_sorteo["ganancias"]
    joker = resultados_sorteo["joker"]
    aciertos = 0
    acierto_comp = 0
    numeros_comp = numeros_p[:6]
    for numero in numeros:
        if numero in numeros_comp:
            aciertos += 1
    if is_comp is True:
        if numeros_p[6] in numeros:
            acierto_comp += 1

    if reintegro == reintegro_p:
        reintegro_acierto = "acertó"
    else:
        reintegro_acierto = "no acertó"

    if joker is False:
        joker_acierto = "No jugó Joker"
    else:
        joker_coincidencias = int()
        for digito in joker_ticket:
            if digito in joker_primi:
                joker_coincidencias += 1
        if joker_ticket == joker_primi:
            joker_acierto = "Premio primera categoría, 1.000.000 €"
        elif joker_ticket[:6] == joker_primi[:6] or joker_ticket[1:] == joker_primi[1:]:
            joker_acierto = "Premio segunda categoría, 10.000 €"
        elif joker_ticket[:5] == joker_primi[:5] or joker_ticket[2:] == joker_primi[2:]:
            if joker_coincidencias == 6:
                joker_acierto = "Premio tercera categoría, 1.001€"
            else:
                joker_acierto = "Premio tercera categoría, 1.000 €"
        elif joker_ticket[:4] == joker_primi[:4] or joker_ticket[3:] == joker_primi[3:]:
            if joker_coincidencias == 6:
                joker_acierto = "Premio cuarta categoría, 305 €"
            elif joker_coincidencias == 5:
                joker_acierto = "Premio cuarta categoría, 301€"
            else:
                joker_acierto = "Premio cuarta categoría, 300 €"
        elif joker_ticket[:3] == joker_primi[:3] or joker_ticket[4:] == joker_primi[4:]:
            if joker_coincidencias == 6:
                joker_acierto = "Premio quinta categoría, 100 €"
            elif joker_coincidencias == 5:
                joker_acierto = "Premio quinta categoría, 55€"
            elif joker_coincidencias == 4:
                joker_acierto = "Premio quinta categoría, 51€"
            else:
                joker_acierto = "Premio quinta categoría, 50 €"
        elif joker_ticket[:2] == joker_primi[:2] and joker_ticket[5:] == joker_primi[5:]:
            joker_acierto = "Premio sexta categoría, 10€"
        elif joker_ticket[:2] == joker_primi[:2] and joker_ticket[6:] == joker_primi[6:]:
            joker_acierto = "Premio sexta categoría, 6€"
        elif joker_ticket[:2] == joker_primi[:2] or joker_ticket[5:] == joker_primi[5:]:
            joker_acierto = "Premio sexta categoría, 5 €"
        elif joker_ticket[:1] == joker_primi[:1] and joker_ticket[6:] == joker_primi[6:]:
            joker_acierto = "Premio séptima categoría, 2€"
        elif joker_ticket[:1] == joker_primi[:1] or joker_ticket[6:] == joker_primi[6:]:
            joker_acierto = "Premio séptima categoría, 1 €"
        else:
            joker_acierto = "Joker no premiado"
    return [aciertos, reintegro_acierto, joker_ticket, joker_acierto, ganancias, acierto_comp]


def premios_resultado():
    """Función para asignar ganancias en base a los aciertos"""

    aciertos, reintegro_acierto, joker_ticket, joker_acierto, ganancias, acierto_comp = primitiva()
    if aciertos == 6 and reintegro_acierto == "acertó":
        pasta = ganancias[0]
    elif aciertos == 6 and reintegro_acierto == "no acertó":
        pasta = ganancias[1]
    elif aciertos == 5 and acierto_comp == 1:
        pasta = ganancias[2]
    elif aciertos == 5:
        pasta = ganancias[3]
    elif aciertos == 4:
        pasta = ganancias[4]
    elif aciertos == 3:
        pasta = ganancias[5]
    elif aciertos <= 2 and reintegro_acierto == "acertó":
        pasta = ganancias[6]
    else:
        pasta = 0

    if joker_ticket is False:
        resultado_joker = "No ha jugado joker"
    else:
        resultado_joker = joker_acierto
    return {"aciertos": aciertos, "pasta": pasta, "joker_ticket": joker_ticket,
            "resultado_joker": resultado_joker, "reintegro_acierto": reintegro_acierto, "acierto_comp": acierto_comp}
# FUNCIÓN EUROMILLONES#########################################################################


# INICIO DEL PROGRAMA#########################################################################
while sorteo != "0":
    print("""
          Bienvenido, por favor, seleccione a que sorteo pertenece el boleto que quiere comprobar
          """)
    # Selección del sorteo
    sorteo = input(
        """Las opciones son: 
        "1": para Primitiva
        "2": para Euromillones
        "3": para Loteria Nacional
        "0": para Salir de la aplicación
        """).lower()
    # sorteo = int(sorteo) --> Eliminado ya que si se meten letras por error el programa peta
    # al comentar esta línea y corregir los if a strings ya funciona. SE CORRIGIÓ
    # DEL MISMO MODO LA OPCIÓN DE JOKER DENTRO DE LA FUNCIÓN PRIMITIVA
    if sorteo == "0":
        print("Gracias por usar esta aplicación")
    elif sorteo == "1":
        print("Ha elegido usted Primitiva, introduzca uno a uno los números de su boleto (1-49)")
        resultado_primitiva = premios_resultado()
        if resultado_primitiva["pasta"] == 0:
            if resultado_primitiva["joker_ticket"] is None:
                print("Combinación de primitiva no premiada")
            else:
                print(f"""
                      Combinación de primitiva no premiada, 
                      Su código joker ha resultado en:{resultado_primitiva["resultado_joker"]}
                    """)
        else:
            print(f"""
                En su ticket de primitiva ha acertado un total de {resultado_primitiva["aciertos"]} numero(s) y
                {resultado_primitiva["reintegro_acierto"]} el reintegro, lo que supone una ganancia económica total de 
                {resultado_primitiva["pasta"]} €.
                """)
            if resultado_primitiva["joker_ticket"] is not None:
                print(f"""
                Su código joker ha resultado en: {resultado_primitiva["resultado_joker"]}
                """)
        sorteo = "0"
        print("Gracias por usar esta aplicación")

    elif sorteo == "2":
        print("Ha elegido usted Euromillones introduzca uno a uno los números de su boleto(1-50)")
    elif sorteo == "3":
        print("Loteria Nacional")
    else:
        print("Ha introducido una opción no válida")
