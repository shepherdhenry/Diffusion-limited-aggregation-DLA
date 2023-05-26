"""
This file is used to generate multiple grid data (.npy)
"""
import numpy as np
import matplotlib.pyplot as plt
import time


start = time.time()

# Parameters
Pnn = 0.3
grid_size = 400
num_particles = 5000
Rmax = 3
particlecount = 0
# Initialize the grid
grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

# Place the initial seed in the center
center = grid_size // 2
grid[center, center] = 1


def aggregate(x, y):
	if (grid[x+1][y] == 1) or (grid[x][y+1] == 1) or (grid[x-1][y] == 1) or (grid[x][y-1] == 1):
		if(np.random.rand()<Pnn):
			return True
	return False


def dla():
	global Rmax
	global particlecount

	while(particlecount<num_particles):
		angle = 2 * np.pi * np.random.rand()
		x = center + int((Rmax+5) * np.cos(angle))
		y = center + int((Rmax+5) * np.sin(angle))


		Notkill = True
		FLAG = True
		while FLAG:

			rand = int(10 * np.random.random())
			if(rand == 0 or rand == 1 or rand == 2 or rand == 3):
				x, y = x-1, y #up
			elif(rand == 6 or rand == 4 or rand == 5 or rand == 7):
				x, y = x+1, y #down
			elif(rand == 8 ):
				x, y = x, y-1 #left
			else:
				x, y = x, y+1 #right
				
			if not ((0 < x < grid_size - 1 and 0 < y < grid_size - 1) and ((x-center)*(x-center)+(y-center)*(y-center)<(3*Rmax)*(3*Rmax))):
				
				Notkill  = False
				break
			


			if ((x-center)*(x-center)+(y-center)*(y-center)<=(Rmax+2)*(Rmax+2)):


				if (grid[x+1][y] == 1) or (grid[x][y+1] == 1) or (grid[x-1][y] == 1) or (grid[x][y-1] == 1):

					grid[x, y] = 1 # particle aggregated
					Notkill = True 
					particlecount += 1
					break	
	

		if(Notkill):
			if abs(x - center) > Rmax or abs(y - center) > Rmax:
				Rmax = max(abs(x - center), abs(y - center))




# Simulate DLA
for _ in range(6,11):
    Rmax = 3
    particlecount = 0
    # Initialize the grid
    grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

    # Place the initial seed in the center
    center = grid_size // 2
    grid[center, center] = 1


    dla()

    #Plot the result
    #plt.imshow(grid, cmap='binary')
    #plt.title('Diffusion-limited aggregation')
    print(particlecount)
    print(time.time()-start)
    #plt.show()

    np.save(f"grid_direction_2_{_}.npy",grid)