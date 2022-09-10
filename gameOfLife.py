import pygame
import numpy
import time

pygame.init()

#background
width, height = 1000, 1000
background = 25, 25, 25
screen = pygame.display.set_mode((height,width))
screen.fill(background)

#cells
nxCells, nyCells = 25, 25
cellWidth = width / nxCells
cellHeight = height / nyCells

gameState=numpy.zeros((nxCells,nyCells))

while True:

    newGameState = numpy.copy(gameState) #copy last state

    time.sleep(0.1)

    screen.fill(background) #clean screen

    #mouse movement and keyboard
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(numpy.floor(posX / cellWidth)), int(numpy.floor(posY / cellHeight))
            newGameState[celX, celY] = 1

    for y in range(0,nxCells):
        for x in range(0,nyCells):
            #calculate number of close cells
            n_neigh =   gameState[(x - 1) % nxCells, (y - 1)  % nyCells] + \
                        gameState[(x)     % nxCells, (y - 1)  % nyCells] + \
                        gameState[(x + 1) % nxCells, (y - 1)  % nyCells] + \
                        gameState[(x - 1) % nxCells, (y)      % nyCells] + \
                        gameState[(x + 1) % nxCells, (y)      % nyCells] + \
                        gameState[(x - 1) % nxCells, (y + 1)  % nyCells] + \
                        gameState[(x)     % nxCells, (y + 1)  % nyCells] + \
                        gameState[(x + 1) % nxCells, (y + 1)  % nyCells]

            #rule 1 : A died cell with 3 live neighbors, relive
            if gameState[x, y] == 0 and n_neigh == 3:
                newGameState[x, y] = 1
            #rule 2 : A live cell with less of 2 or 3 live neighbors, dies
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newGameState[x, y] = 0


            #polygon cell
            poly = [((x)*cellWidth, (y)*cellHeight),
                    ((x+1)*cellWidth, (y)*cellHeight),
                    ((x+1)*cellWidth, (y+1)*cellHeight),
                    ((x)*cellWidth, (y+1)*cellHeight),]

            #if cell is die => grey border
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (40, 40, 40), poly, 1)
            else:
                pygame.draw.polygon(screen, (200, 100, 100), poly, 0)

    gameState = numpy.copy(newGameState)

    pygame.display.flip()