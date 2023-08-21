import pygame
import random
import sys

blanco = (255,255,255)
negro = (0,0,0)
mapColor = (200,200,200)
cellSize = 40
matriz = []
mDistancias = []

def xyCuadricula (cols, rows):
    matriz.clear()
    for i in range (cols):
        x = i * cellSize + cellSize // 2
        for j in range (rows):
            y = j * cellSize + cellSize // 2
            matriz.append([x,y])

#def posiciones(rows, cols):
#    fila = random.randint(0, rows - 1)
#    columna = random.randint(0, cols - 1)
#    
#    x = columna * cellSize + cellSize // 2
#    y = fila * cellSize + cellSize // 2
#    pos = (x, y)
#    return pos


def drawVacuum(screen, pos):
    for location in pos:
        pygame.draw.circle(screen,negro, location, 12)

def drawDirty(screen, pos):
    for location in pos:
        pygame.draw.rect(screen, negro, pygame.Rect(location[0] - 10, location[1] - 10, 20, 20))

def mapeado(screen,screenW,screenH):
    for x in range(0, screenW, cellSize):
        pygame.draw.line(screen, mapColor, (x, 0), (x, screenH))
    for y in range(0, screenH, cellSize):
        pygame.draw.line(screen, mapColor, (0, y), (screenW, y))

def distancias(posVacuums, posDirty):
    for pos1 in posVacuums:
        distans = []
        for pos2 in posDirty:
            distan = ((pos2[0] - pos1[0]) **2 + (pos2[1] - pos1[1]) ** 2) ** 0.5
            distans.append(distan)
        mDistancias.append(distans)

def movimiento(posVacuums, posDirty):
    for i in range(len(posVacuums)):
        xActual, yActual = posVacuums[i]
        xSiguiente, ySiguiente = posDirty[i]

        if xActual < xSiguiente:
            posVacuums[i] = (xActual + 1, yActual)
        elif xActual > xSiguiente:
            posVacuums[i] = (xActual - 1, yActual)

        if yActual < ySiguiente:
            posVacuums[i] = (xActual, yActual + 1)
        elif yActual > ySiguiente:
            posVacuums[i] = (xActual, yActual - 1)

def asignarPosicionesSucias(posDirty, posVacuums):
    posiciones_disponibles = posDirty.copy()
    posiciones_asignadas = []

    for vacuum_pos in posVacuums:
        if posiciones_disponibles:
            min_distance = float('inf')
            nearest_dirty = None

            for dirty_pos in posiciones_disponibles:
                distance = ((vacuum_pos[0] - dirty_pos[0]) ** 2 + (vacuum_pos[1] - dirty_pos[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_dirty = dirty_pos

            posiciones_asignadas.append(nearest_dirty)
            posiciones_disponibles.remove(nearest_dirty)
        else:
            posiciones_asignadas.append(vacuum_pos)

    return posiciones_asignadas

def main():
    cols = int(input("Ingresa el numero de columnas: "))
    rows = int(input("Ingresa el numero de filas: "))
    vacuums = int(input("Ingresa el numero de aspiradoras: "))
    espaciosSucios = int(input("Ingresa el numero de espacios sucios: "))
    obstaculos = 0

    xyCuadricula(cols,rows)

    posVacuums = []
    for _ in range (vacuums):
        cuadro = random.randint(0,len(matriz)-1)
        lVacuums = matriz[cuadro]
        posVacuums.append(lVacuums)
    
    print (posVacuums)

    posDirty = []
    for _ in range (espaciosSucios):
        cuadro = random.randint(0,len(matriz)-1)
        lDirty = matriz[cuadro]
        posDirty.append(lDirty)

    print (posDirty)

    posiciones_asignadas = asignarPosicionesSucias(posDirty, posVacuums)

    pygame.init()
    size = (cols * cellSize, rows*cellSize)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Vaccum World")
    clock = pygame.time.Clock()
    gameOver = False

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True

        screen.fill(blanco)
        mapeado(screen, cols * cellSize, rows * cellSize)
        drawVacuum(screen, posVacuums)
        drawDirty(screen, posiciones_asignadas)
        movimiento(posVacuums, posiciones_asignadas)
        pygame.display.flip()
        clock.tick(12)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()