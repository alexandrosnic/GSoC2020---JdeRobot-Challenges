import numpy as np 
import json
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import random

# Read the pattern
with open('patterns.json', 'r') as f:
    patterns_dict = json.load(f)
print('Choose a pattern: 0: toad, 1: beacon, 2: glider, 3: board')
patNum=int(input())
if patNum < 4 and patNum >=0:
    currentGrid = patterns_dict[patNum]['pattern']
else:
    patNum =random.randint(0,3)
    print('Invalid pattern. Another one was chosen')
    currentGrid = patterns_dict[patNum]['pattern']

# Pattern properties
global rowSize, colSize 
rowSize = len(patterns_dict[patNum]['pattern'])
colSize = len(patterns_dict[patNum]['pattern'][0])

# Initialise the nextgrid
nextgrid = []
for row in range(0,rowSize):
    nextgrid.append([])
    for col in range(0,colSize):
        nextgrid[row].append(0)

#Generate Next Grid using the four key rules of Conway's Game of Life
def update(data):
    global currentGrid
    global nextgrid
    for i in range(0,rowSize):
        for j in range(0,colSize):
            # Count the number of neighbors
            neighbors = (currentGrid[i][ (j-1)%colSize] + currentGrid[i][ (j+1)%colSize] + currentGrid[(i-1)%rowSize][ j] + currentGrid[(i+1)%rowSize][ j] + currentGrid[(i-1)%rowSize][ (j-1)%colSize] + currentGrid[(i-1)%rowSize][ (j+1)%colSize] + currentGrid[(i+1)%rowSize][ (j-1)%colSize] + currentGrid[(i+1)%rowSize][ (j+1)%colSize])
            # apply Conway's rules
            if currentGrid[i][ j]  == 1:
                if (neighbors < 2) or (neighbors > 3):
                    nextgrid[i][ j] = 0
            else:
                if neighbors == 3:
                    nextgrid[i][ j] = 1

    tmpgrid = currentGrid
    currentGrid = nextgrid
    nextgrid=tmpgrid
    matrice.set_data(currentGrid)
    return [matrice]

# Plot the updated grid
fig, ax = plt.subplots()
matrice = ax.matshow(currentGrid)
ani = animation.FuncAnimation(fig, update, frames=10, interval=100 )
plt.show()

