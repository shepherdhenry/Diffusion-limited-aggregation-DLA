"""
This program is used to calcuate the C(r)(c) and fratcal dimension (d)
"""

############import####################
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
######################################

#grid paremter
grid_num = 5
grid_size = 500
center = grid_size // 2

#valid points to calculate linear fit function
#vaild = 10 #Pnn = 1
vaild = 16 #Pnn = 0.3
step = 6

#ininialization
grid_array = np.zeros((grid_num,grid_size,grid_size))
a_list = []
b_list = []
coeff_list = []
error_list = []
R_list=np.arange(26,grid_size//2-1,step)
lnR_list = np.log(R_list)

# compute the N(r) and C(r)
for i in range(1, grid_num+1):
    #get grid
    #grid = np.load(f"grid_data\grid1_{i}.npy") # Pnn = 1
    grid = np.load(f"grid_data\grid_snn_nn_03_{i}.npy") # Pnn = 0.3
    
    grid_array[i-1] = grid

    count_list = []

    # count all particles with R
    for R in R_list:
        count = 0
        
        for i in range(center-R, center+R+1):
            for j in range(center-R, center+R+1):
                
                if ((i-center)*(i-center) + (j-center)*(j-center) <= R*R):
                    count += grid[i][j]
        count_list.append(count)
        

    # calculate the function of N(r)
    count_list = np.log(count_list)

    coeff,error,rank, singular_values, rcond = np.polyfit(lnR_list[:vaild], count_list[:vaild], 1, full=True)
    coeff_list.append(coeff)
    error_list.append(error)
    print(f"fratcal dimension is {coeff[0]}")

    # calculate the C(r) from N(r)
    # suppose C(r) = C*r^a
    # lnC(r) = a*lnr + a*lnC, make a*lnC = b

    a = coeff[0]-2
    b = np.log(coeff[0]/(2*np.pi))+coeff[1]
    a_list.append(a)
    b_list.append(b)
    print(f"alpha is {a}")

# find mean grid to plot scatter figure
grid_mean = np.mean(grid_array, axis=0)
count_list = []
for R in R_list:
    count = 0
    
    for i in range(center-R, center+R+1):
        for j in range(center-R, center+R+1):
            
            if ((i-center)*(i-center) + (j-center)*(j-center) <= R*R):
                count += grid_mean[i][j]
    count_list.append(count)
count_list = np.log(count_list) 

#Plot the result
a = np.mean(a_list)
b = np.mean(b_list)
coeff = np.mean(coeff_list, axis=0)
error = np.linalg.norm(error, 2)/(grid_num-1)
lnC = a*lnR_list + b
lnN = coeff[0]*lnR_list + coeff[1]
roundpoint = 3
plt.subplot(121)
plt.title("Density function")
plt.plot(lnR_list[:vaild], lnC[:vaild])
plt.text(4,-1.9,f'ln(C(r))=({round(a,roundpoint)}±{round(error,roundpoint)})*lnr + {round(b,roundpoint)}',fontdict={'size':'8','color':'b'})
plt.xlabel("lnr")
plt.ylabel("lnC(r)")

plt.subplot(122)
plt.title("Number of particles with R")
plt.plot(lnR_list[:vaild], lnN[:vaild],linestyle = '--',color='r')
plt.scatter(lnR_list, count_list)
plt.xlabel("lnr")
plt.ylabel("lnN(r)")
plt.text(4.4,8.4,f'ln(N(r))=({round(coeff[0],roundpoint)}±{round(error,roundpoint)})*lnr + {round(coeff[1],roundpoint)}',fontdict={'size':'8','color':'r'})
print(f"fratcal dimension is {coeff[0]}")
print(f"alpha is {a}")
print(f"error is {error}")
plt.show()