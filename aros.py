#!/usr/env python3
# -*- encoding: UTF-8 -*-

import os
import time
import curses
import platform
import copy

aro = "0"
palo = "|"
base = "="
vacio = " "
numAros = 5
numPalos = 3
distancia = 3
scorefilePath = "./score.txt"
menu = """
    Menu de opciones:

    0) Jugar
    1) Ver puntajes
    q) Salir
"""

pantalla = curses.initscr()

def esperarTecla(x, y, permitidas=""):
    if permitidas == "":
        permitidas = [chr(ch) for ch in range(32, 128)]
    try:
        pantalla = curses.initscr()
        while True:
            pantalla.addstr(x, y, "")
            ch = chr(pantalla.getch())
            pantalla.addstr(x, y, "")
            if ch in permitidas:
                break
            time.sleep(0.05)
    except:
        raise
    finally:
        curses.endwin()
    return ch

def dibujar(dibujo):
    pantalla.addstr(0, 0, dibujo)

def generarPalos():
    salida = []
    salida.append(list(range(1, numAros+1)))
    for i in range(0, numPalos-1):
        salida.append([]) #0 for x in range(0, numAros)])
    return salida

def generarDibujo(palos, distancia, altura):
    salida = []
    ancho = 3 + (numAros*2)

    montones = copy.deepcopy(palos)
    for i in range(0, len(palos)):
        ceros = []
        for x in range(0, altura-len(montones[i])):
            ceros.append(0)
        montones[i] = ceros + montones[i]
    linea = "{0}{1}{2}".format(
        vacio*distancia + vacio*int(ancho/2),
        palo,
        vacio*int(ancho/2),
    )
    salida.append(linea*numPalos)
    for posicion in range(0, numAros):
        linea = vacio*distancia
        for monton in montones:
            if monton[posicion] == 0:
                dibujoAro = palo
            else:
                dibujoAro = aro*(1 + 2*monton[posicion])
            espacioLateral = vacio*(numAros - monton[posicion] + 1)
            linea += espacioLateral + dibujoAro + espacioLateral + vacio*distancia
        salida.append(linea)
    linea = vacio*distancia + base*(ancho)
    salida.append(linea*numPalos)
    return salida

def actualizar(palos, nummov):
    dibujo = generarDibujo(palos, distancia, 5)
    dibujado = ""
    for linea in dibujo:
        dibujado += linea + "\n"
    dibujar(dibujado)
    pantalla.addstr(numAros+3, 0, "Movimientos: {0}".format(nummov))

def clear():
    pantalla.clear()

def jugar():
    clear()
    palos = generarPalos()
    nummov = 0
    actualizar(palos, nummov)
    tecla_anterior = ""
    while len(palos[2]) != 5:
        teclas = ["", "x"]
        while teclas[1] == "x" or teclas[0] == teclas[1]:
            teclas[0] = esperarTecla(0, 0, "123q")
            if teclas[0] == "q":
                pantalla.addstr(numAros+4, 3, "Presiona 'q' otra vez para salir, 'x' para cancelar")
                if esperarTecla(0, 0, "qx") == "q":
                    break
                else:
                    pantalla.addstr(numAros+4, 3, "                                                   ")
                    continue
            ancho = (3 + (numAros*2))
            linea = "{0}^".format(" "*((int(teclas[0]) - 1)*(ancho + distancia) + int(ancho/2) + distancia))
            pantalla.addstr(numAros+2, 0, linea)
            teclas[1] = esperarTecla(0, 0, "123x")
            linea = "{0} ".format(" "*((int(teclas[0]) - 1)*(ancho + distancia) + int(ancho/2) + distancia))
            pantalla.addstr(numAros+2, 0, linea)
        if teclas[0] == "q": break
        mov = [
            int(teclas[0])-1,
            int(teclas[1])-1,
        ]
        if len(palos[mov[0]]) != 0 and (len(palos[mov[1]]) == 0 or palos[mov[1]][0] > palos[mov[0]][0]):
            aux = palos[mov[0]].pop(0)
            palos[mov[1]].insert(0, aux)
            clear()
            nummov += 1
            actualizar(palos, nummov)
        else:
            pantalla.addstr(numAros+4, 3, "Movimiento ilegal")
    if teclas[0] == "q":
        return
    pantalla.addstr(numAros+4, 3, "Ganaste en {0} movimientos. Presiona una tecla...".format(nummov))
    esperarTecla(0, 0)
    clear()
    pantalla.addstr(2, 3, "Ingresa tu nombre")
    nombre = leerEntrada(4, 0, "--> ", 3, True)
    score = open(scorefilePath, "a")
    score.write("{0}:{1}\n".format(nombre, nummov))
    score.close()

def leerEntrada(x, y, prompt="", maximo=-1, capitalize=False, chrpermitidos="abcdefghijklmnopqrstuvwxyzñ0123456789", chrfinal="\n", chrborrar="\x7f"):
    salida = ""
    lineas = prompt.split("\n")
    xfin = len(lineas) - 1 + x
    yfin = len(lineas[len(lineas)-1]) + y
    while True:
        pantalla.move(xfin, yfin)
        pantalla.deleteln()
        if capitalize:
            txt = "".join([ch.capitalize() for ch in salida])
        else:
            txt = salida
        pantalla.addstr(x, y, prompt+txt)
        tecla = esperarTecla(xfin, yfin, chrpermitidos+chrfinal+chrborrar)
        if tecla == chrborrar and len(salida) > 0:
            salida = salida[:len(salida)-1]
        elif tecla == chrfinal:
            break
        elif len(salida) < maximo and tecla != chrborrar:
            salida += tecla
    return salida

def verScore():
    clear()
    pantalla.addstr(2, 3, "Seleccione el jugador (vacío para mostrar todos)")
    nombre = leerEntrada(4, 0, "--> ", 3, True)
    f = open(scorefilePath, "r")
    score = f.read()
    f.close()
    datos = {}
    for p in score.split("\n"):
        registro = p.split(":")
        if p != "" and (nombre == "" or registro[0] == nombre):
            if not registro[0] in datos:
                datos[registro[0]] = []
            datos[registro[0]].append(registro[1])
    #TODO: Mostrar resultados
    salida = ""
    for p, s in datos.items():
        minimo = int(s[0])
        maximo = 0
        promedio = 0
        jugadas = 0
        for v in s:
            jugadas += 1
            valor = int(v)
            if valor < minimo:
                minimo = valor
            if valor > maximo:
                maximo = valor
            promedio += valor
        promedio = promedio/len(s)
        salida += "{0}: {1}, {2}, {3} ({4})\n".format(
            "".join([ch.capitalize() for ch in p]),
            minimo,
            maximo,
            promedio,
            jugadas,
            )
    clear()
    dibujar(salida+"\nPresiona una tecla...")
    esperarTecla(0, 0)

def main():
    opciones = [
        jugar,
        verScore,
    ]
    while True:
        clear()
        #TODO: Mostrar menu de opciones
        tecla_presionada = leerEntrada(0, 0, menu+"\n--> ", 1, True)
        try:
            opcion = int(tecla_presionada)
            opciones[opcion]()
        except Exception:
            opcion = tecla_presionada
            if opcion == "q":
                break
    clear()
    dibujar(" Bai bai xdxd")
    esperarTecla(0, 0, "abcdefghijklmnopqrstuvwxyzñ0123456789\n")

if __name__ == "__main__":
    main()
    print("FIN :)")
