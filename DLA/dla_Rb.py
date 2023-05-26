"""
PHYS 3142 FINAL RROJECT:

Diffusion-limited aggregation

This file is used to set a real boundary Rb

Paramter:
	grid: a simple lattice (cluster)
	grid_size: the length of grid length
	Rmax:  the maximum distance from the seed to the outermost particle
	particlecount: the number of particle in cluster
	Pnn: the sticking probability at the nearest neighbor sites 
	Psnn: the sticking probability at the second nearest neighbor sites 

"""
### import #########################
import numpy as np
import matplotlib.pyplot as plt
import time
####################################

start = time.time()




##############Initialization##################
# initialize Parameters
Pnn = 1
grid_size = 300
num_particles = 9000
Rmax = 3
Rb = 125
particlecount = 0

# Initialize the grid
grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

# Place the initial seed in the center
center = grid_size // 2
grid[center, center] = 1
##############################################





# function to randomly generate a particle at random pos(x,y)
# acctually not be implemented to save run time !!!
def random_generate():
	angle = 2 * np.pi * np.random.rand()
	x = center + int((Rmax+5) * np.cos(angle))
	y = center + int((Rmax+5) * np.sin(angle))
	return x,y

# function to estimate that whether a particle should be killed(out of 3*Rmax or out of grid)
# acctually not be implemented to save run time !!!
def in_bounds(x, y):
    
	if(0 < x < grid_size - 1 and 0 < y < grid_size - 1) \
		and ((x-center)*(x-center)+(y-center)*(y-center)<(3*Rmax)*(3*Rmax)):

		return True
	return False

# function to estimatethat whether a particle aggregate
def aggregate(x, y):
	if (grid[x+1][y] == 1) or (grid[x][y+1] == 1) or (grid[x-1][y] == 1) or (grid[x][y-1] == 1):
		return True
	return False

# simulation of Diffusion-limited aggregation
def dla():
	# global function to update paramter
	global Rmax
	global particlecount

	# ensure there is num_particles in the cluster
	while( particlecount < num_particles ):

		#randomly generate a particle at random pos(x,y)
		angle = 2 * np.pi * np.random.rand()
		x = center + int((Rmax+5) * np.cos(angle))
		y = center + int((Rmax+5) * np.sin(angle))


		Notkill = True
		FLAG = True
		# simulate the process of random walk
		while FLAG:

			# random walk
			rand = int(4 * np.random.random())
			if(rand == 0):
				x, y = x-1, y
			elif(rand == 1):
				x, y = x+1, y
			elif(rand == 2):
				x, y = x, y-1
			else:
				x, y = x, y+1
			
			# estimate that whether a particle should be killed(out of 3*Rmax or out of grid)
			if not (center-Rb < x <  center +Rb and center - Rb < y < center + Rb):
				
				Notkill  = False
				break
			

			#  checking of the nearest neighbor sites is started if 
			# 	the particle reaches the distance 𝑅𝑚𝑎𝑥 + 2 from the cluster
			if ((x-center)*(x-center)+(y-center)*(y-center)<=(Rmax+2)*(Rmax+2)):



				if (grid[x+1][y] == 1) or (grid[x][y+1] == 1) or (grid[x-1][y] == 1) or (grid[x][y-1] == 1):
					
					grid[x, y] = 1 # particle aggregated
					Notkill = True 
					particlecount += 1

					break	
	
		# if particle is not killed, update Rmax
		if(Notkill):
			if abs(x - center) > Rmax or abs(y - center) > Rmax:
				Rmax = max(abs(x - center), abs(y - center))
		



# Simulate DLA
dla()

print("Pnn = 1")
print(f"The number of particle in cluster is {particlecount}")
print(f"The simulate cost {time.time()-start}s")

#Plot the result
plt.imshow(grid, cmap='binary')
plt.colorbar()
plt.title('Diffusion-limited aggregation (Pnn=1)')
plt.show()

np.save(f"grid_Rb_{7}.npy", grid)