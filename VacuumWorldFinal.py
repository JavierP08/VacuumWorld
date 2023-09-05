#   VacuumWorld 
#       Simulación donde difrentes agentes(Aspiradoras) 
#       tienen como objetivo limpiar su ambiente.
#   Liliana Hernández García A01640873
#   Javier Pérez Santiago A01662438
#   20 de Agosto de 2023

import pygame
import random
import sys

# Constantes del programa 
BLANCO = (255,255,255)
NEGRO = (0,0,0)
MAPCOLOR = (200,200,200)
CELSIZE = 40
MATRIZ = []
MDISTANCIAS = []
ESPACIOSlIMPIOS = []

# Función que obtiene la posición exacta de cada uno de los recuadros de la cuadrícula 
def xyCuadricula (cols, rows):
    MATRIZ.clear()
    for i in range (cols):
        x = i * CELSIZE + CELSIZE // 2
        for j in range (rows):
            y = j * CELSIZE + CELSIZE // 2
            MATRIZ.append([x,y])

# Función para el dibujo de las Vacuum(Aspiradoras)
def drawVacuum(screen, pos):
    for location in pos:
        pygame.draw.circle(screen,NEGRO, location, 12)

# Función para el dibujo de los espacios sucios (Dirty)
def drawDirty(screen, posDirty):
    for location in posDirty:
        if location not in ESPACIOSlIMPIOS:
            pygame.draw.rect(screen, NEGRO, pygame.Rect(location[0] - 10, location[1] - 10, 20, 20))

# Función que realiza el mapeado, o sea la cudrícula del ambiente
def mapeado(screen,screenW,screenH):
    for x in range(0, screenW, CELSIZE):
        pygame.draw.line(screen, MAPCOLOR, (x, 0), (x, screenH))
    for y in range(0, screenH, CELSIZE):
        pygame.draw.line(screen, MAPCOLOR, (0, y), (screenW, y))

# Función que nos ayuda a obtener la distancia entre un Vacuum y una posición Dirty
def distancias(posVacuums, posDirty):
    for pos1 in posVacuums:
        distans = []
        for pos2 in posDirty:
            distan = ((pos2[0] - pos1[0]) *2 + (pos2[1] - pos1[1]) * 2) ** 0.5
            distans.append(distan)
        MDISTANCIAS.append(distans)

# Función que realiza el movimiento del Vacuum hacia la posición Dirty
def movimiento(posVacuums, posDirty, posAsignada, pasos):
    aspiradoraMover = []  # Lista auxiliar para almacenar aspiradoras y sus posiciones asignadas

    for i in range(len(posVacuums)):
        xActual, yActual = posVacuums[i]
        xSiguiente, ySiguiente = posAsignada[i]

        if (xActual, yActual) != (xSiguiente, ySiguiente):
            # Mover la aspiradora hacia su posición asignada
            if xActual < xSiguiente:
                posVacuums[i] = (xActual + 1, yActual)
            elif xActual > xSiguiente:
                posVacuums[i] = (xActual - 1, yActual)

            if yActual < ySiguiente:
                posVacuums[i] = (xActual, yActual + 1)
            elif yActual > ySiguiente:
                posVacuums[i] = (xActual, yActual - 1)

            pasos[i] += 1  # Aumentar el contador de pasos para esta aspiradora

        else:
            # La aspiradora ha llegado a su posición asignada
            if posAsignada[i] in posDirty:  # Revisa si la posición todavía está sucia
                ESPACIOSlIMPIOS.append(posAsignada[i])
                posDirty.remove(posAsignada[i])
            else:
                aspiradoraMover.append(i)  # Agrega la aspiradora que no ha llegado a su posición

    # Resto del código
  # Agrega la aspiradora que no ha llegado a su posición

    # Actualiza las listas principales con las aspiradoras y posiciones asignadas que necesitan moverse
    nuevaPosVacuum = [posVacuums[i] for i in aspiradoraMover]
    nuevaPosAsignada = [posAsignada[i] for i in aspiradoraMover]

    return nuevaPosVacuum, nuevaPosAsignada


# Función que nos ayuda a asignarle a cada Vacuum un posición Dirty
def asignarPosicionesSucias(posDirty, posVacuums):
    posAsignada = []  # Lista para almacenar las posiciones asignadas a las aspiradoras
    posDisponibles = posDirty.copy()  # Copia de las posiciones sucias disponibles

    for vacuumPos in posVacuums:
        if posDisponibles:
            distanciaMinima = float('inf')
            dirtyMasCercano = None

            for dirtyPos in posDisponibles:
                # Calcula la distancia euclidiana entre las posiciones
                distance = ((vacuumPos[0] - dirtyPos[0]) ** 2 + (vacuumPos[1] - dirtyPos[1]) ** 2) ** 0.5
                if distance < distanciaMinima:
                    distanciaMinima = distance
                    dirtyMasCercano = dirtyPos

            posAsignada.append(dirtyMasCercano)
            posDisponibles.remove(dirtyMasCercano)
        else:
            posAsignada.append(vacuumPos)  # Si no hay posiciones sucias, se mantiene la posición de la aspiradora

    return posAsignada


# Main
def main():
    # Inputs
    cols = int(input("Ingresa el numero de columnas: "))
    rows = int(input("Ingresa el numero de filas: "))
    vacuums = int(input("Ingresa el numero de aspiradoras: "))
    espaciosSucios = int(input("Ingresa el numero de espacios sucios: "))
    steps = int(input("Dime el numero de steps que quieres que tenga: "))

    steps = steps * 40
    
    pasos = [0] * vacuums

    # Llamada a la funcion para obtener las posiciones de los cuadros del mapa
    xyCuadricula(cols,rows)

    # Asiganción de las posiciones de las Vacuums
    posVacuums = []
    for _ in range (vacuums):
        cuadro = random.randint(0,len(MATRIZ)-1)
        lVacuums = MATRIZ[cuadro]
        posVacuums.append(lVacuums)

    # Asignación de las posiciones Dirty
    posDirty = []
    for _ in range (espaciosSucios):
        cuadro = random.randint(0,len(MATRIZ)-1)
        lDirty = MATRIZ[cuadro]
        posDirty.append(lDirty)

    # Asigancion de la posición Dirty a cada Vacuum mediante de la función asignarPosicionesSucias()
    posAsignada = asignarPosicionesSucias(posDirty, posVacuums)

    # Inicio de display que nos ayuda a hacer la simulación
    # Lo que utilizamos nosotros fue pygame
    pygame.init()
    size = (cols * CELSIZE, rows*CELSIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Vaccum World")
    clock = pygame.time.Clock()
    gameOver = False
    paused = False

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True

        screen.fill(BLANCO)
    
        if not paused:
            # Llamada a las diferentes funciones que nos ayudaran a:
                # 1. El mapeado del ambiente
            mapeado(screen, cols * CELSIZE, rows * CELSIZE)

                # 2. Dibujar las Aspiradoras
            drawVacuum(screen, posVacuums)

                # 3. Dibujar los espacios sucios
            drawDirty(screen, posAsignada)

                # 4. Mover las aspiradoras a los espacios sucios
            movimiento(posVacuums, posDirty, posAsignada, pasos)

            if pasos[vacuums-1] == steps:
                paused = True
        else:
            mapeado(screen, cols * CELSIZE, rows * CELSIZE)
            drawVacuum(screen, posVacuums)
            drawDirty(screen, posAsignada)
        
        pygame.display.flip()
        clock.tick(60)
    for i in range(vacuums):
        print(f"Aspiradora {i + 1} tardó {(pasos[i])//40} pasos en llegar a su destino.")
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()