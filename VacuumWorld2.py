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

def distancia_euclidiana(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

def movimiento(vacuum_pos, dirty_pos):
    closest_dirty = None
    min_distance = float('inf')
    
    for dirty in dirty_pos:
        for vacuum in vacuum_pos:
            dist = distancia_euclidiana(vacuum, dirty)
            if dist < min_distance:
                min_distance = dist
                closest_dirty = dirty
    
    if closest_dirty:
        dx = closest_dirty[0] - vacuum_pos[0]
        dy = closest_dirty[1] - vacuum_pos[1]
        if abs(dx) > abs(dy):
            if dx > 0:
                vacuum_pos[0] += cellSize
            else:
                vacuum_pos[0] -= cellSize
        else:
            if dy > 0:
                vacuum_pos[1] += cellSize
            else:
                vacuum_pos[1] -= cellSize

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
        mapeado(screen, cols*cellSize, rows*cellSize)

        for i in range(vacuums):
            drawVacuum(screen, [posVacuums[i]])
            drawDirty(screen, posDirty)
            movimiento(posVacuums[i], posDirty)
            pygame.display.flip()
            clock.tick(10)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()