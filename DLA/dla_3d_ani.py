"""
PHYS 3142 FINAL RROJECT:

Diffusion-limited aggregation

This file is used to make 3D animation

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
import imageio
import os
####################################

start = time.time()




##############Initialization##################
# initialize Parameters
Pnn = 1
grid_size = 100
num_particles = 2000
Rmax = 3
particlecount = 0
needGif = True
# Initialize the grid
grid = np.zeros((grid_size, grid_size, grid_size))

# Place the initial seed in the center
center = grid_size // 2
grid[center, center, center] = 1
##############################################





# function to randomly generate a particle at random pos(x,y)
# acctually not be implemented to save run time !!!
def random_generate():
	theta = 2 * np.pi * np.random.rand()
	phi = np.pi * np.random.rand()
	x = center + int((Rmax+5) * np.cos(phi)*np.sin(theta))
	y = center + int((Rmax+5) * np.sin(phi)*np.sin(theta))
	z = center + int((Rmax+5) * np.cos(theta))
	return x,y,z

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

Interval = []
# simulation of Diffusion-limited aggregation
def dla():
	# global function to update paramter
    global particlecount
    global Rmax
    global needGif
    intervalSavePic = range(1,3000-1,25)
    k=0
	# ensure there is num_particles in the cluster
    while( particlecount < num_particles):

		#randomly generate a particle at random pos(x,y)
        theta = 2 * np.pi * np.random.rand()
        phi = np.pi * np.random.rand()
        x = center + int((Rmax+5) * np.cos(phi)*np.sin(theta))
        y = center + int((Rmax+5) * np.sin(phi)*np.sin(theta))
        z = center + int((Rmax+5) * np.cos(theta))

        Notkill = True
        FLAG = True
        # simulate the process of random walk
        while FLAG:

            # random walk
            rand = int(6 * np.random.random())
            if(rand == 0):
                x, y, z = x-1, y, z
            elif(rand == 1):
                x, y, z = x+1, y, z
            elif(rand == 2):
                x, y, z = x, y-1, z
            elif(rand == 3):
                x, y, z = x, y+1, z
            elif(rand == 4):
                x, y, z = x, y, z+1
            else:
                x, y, z = x, y, z-1
            
            # estimate that whether a particle should be killed(out of 3*Rmax or out of grid)
            if not ((0 < x < grid_size - 1 and 0 < y < grid_size - 1 and 0 < z < grid_size - 1)): #\
                #and ((x-center)*(x-center)+(y-center)*(y-center)+ (z-center)*(z-center)<(5*Rmax)*(5*Rmax))):
                
                Notkill  = False
                break
            

            #  checking of the nearest neighbor sites is started if 
            # 	the particle reaches the distance 𝑅𝑚𝑎𝑥 + 2 from the cluster
            if ((x-center)*(x-center)+(y-center)*(y-center)+(z-center)*(z-center)<=(Rmax+2)*(Rmax+2)):



                if (grid[x+1][y][z] != 0) or (grid[x][y+1][z] != 0) or (grid[x-1][y][z] != 0) \
                    or (grid[x][y-1][z] != 0) or (grid[x][y][z+1] != 0) or (grid[x][y][z-1] != 0):
                    
                    grid[x, y, z] = (num_particles-particlecount)/num_particles #1 # particle aggregated
                    Notkill = True 
                    particlecount += 1

                    break	

        # if particle is not killed, update Rmax
        if(Notkill):
            if abs(x - center) > Rmax or abs(y - center) or abs(z - center)  > Rmax:
                Rmax = max(abs(x - center), abs(y - center), abs(z - center))

            if particlecount in intervalSavePic:
                print("still working, have added ",  " Added to cluster: ", particlecount)

            if needGif:
                if particlecount in intervalSavePic:
                    print("save picture")
                    Interval.append(particlecount) #append to the used count

                    latticePlot = np.nonzero(grid)
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    cmap = plt.cm.plasma
                    colourArrangement = np.zeros(np.shape(latticePlot)[1])
                    for n in range(np.shape(latticePlot)[1]):
                        colourArrangement[n] = grid[latticePlot[0][n],latticePlot[1][n],latticePlot[2][n]]
                    ax.scatter(latticePlot[2],latticePlot[1],latticePlot[0],c=colourArrangement,cmap='plasma',marker='s')
                    plt.title('3D DLA')

                    plt.savefig("images/cluster3d{}.png".format(k), dpi=200)
                    k+=1
                    plt.close()





# Simulate DLA
dla()

print("Pnn = 1")
print(f"The number of particle in cluster is {particlecount}")
print(f"The simulate cost {time.time()-start}s")

latticePlot = np.nonzero(grid)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
cmap = plt.cm.plasma
colourArrangement = np.zeros(np.shape(latticePlot)[1])
for n in range(np.shape(latticePlot)[1]):
    colourArrangement[n] = grid[latticePlot[0][n],latticePlot[1][n],latticePlot[2][n]]
ax.scatter(latticePlot[2],latticePlot[1],latticePlot[0],c=colourArrangement,cmap='plasma',marker='s')
plt.title('3D DLA')
plt.savefig("images/cluster3d.png", dpi=200)

if needGif:
    with imageio.get_writer('images/movie3d.gif', mode='I') as writer:
        j=0
        for i in Interval:
            filename="images/cluster3d"+str(j)+".png"
            image = imageio.imread(filename)
            writer.append_data(image) 
            j+=1          
        image = imageio.imread("images/cluster3d.png")
        writer.append_data(image)

for i in Interval:
    filename="images/cluster"+str(i)+".png"
    os.remove(filename)