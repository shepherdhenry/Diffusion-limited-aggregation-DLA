"""
This program is used to calcuate the 3D C(r)(c) and fratcal dimension (d)
"""

############import####################
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
######################################

#grid paremter
grid_num = 10
grid_size = 150
center = grid_size // 2

#valid points to calculate linear fit function
vaild = 10
step = 1

#ininialization
grid_array = np.zeros((grid_num,grid_size,grid_size,grid_size))
a_list = []
b_list = []
coeff_list = []
error_list = []
R_list=np.arange(step,grid_size//3,step)
lnR_list = np.log(R_list)

# compute the N(r) and C(r)
for i in range(1, grid_num+1):
    #get grid
    grid = np.load(f"grid_data\grid_3d_{i}.npy") # Pnn = 1
    
    grid_array[i-1] = grid

    count_list = []

    # count all particles with R
    for R in R_list:
        count = 0
        
        for i in range(center-R, center+R+1):
            for j in range(center-R, center+R+1):
                for k in range(center-R, center+R+1):
                    
                    if ((i-center)*(i-center) + (j-center)*(j-center) + (k-center)*(k-center) <= R*R):
                        count += grid[i][j][k]
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

    a = coeff[0]-3
    b = np.log(coeff[0]/(4*np.pi))+coeff[1]
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
            for k in range(center-R, center+R+1):
                
                if ((i-center)*(i-center) + (j-center)*(j-center) + (k-center)*(k-center) <= R*R):
                    count += grid[i][j][k]
    count_list.append(count)
count_list = np.log(count_list) 

#Plot the result
a = np.mean(a_list)
b = np.mean(b_list)
coeff = np.mean(coeff_list, axis=0)
error = np.linalg.norm(error, 2)/(grid_num-1)
lnC = a*lnR_list + b
lnN = coeff[0]*lnR_list + coeff[1]

plt.subplot(121)
plt.title("density function")
plt.plot(lnR_list[:vaild], lnC[:vaild])
plt.text(1,-0.8,f'ln(C(r))=({round(a,2)}±{round(error,2)})*lnr + {round(b,2)}',fontdict={'size':'10','color':'b'})
plt.xlabel("lnr")
plt.ylabel("lnC(r)")

plt.subplot(122)
plt.plot(lnR_list[:vaild], lnN[:vaild],linestyle = '--',color='r')
plt.scatter(lnR_list, count_list)
plt.xlabel("lnr")
plt.ylabel("lnN(r)")
plt.text(2,5,f'ln(N(r))=({round(coeff[0],2)}±{round(error,2)})*lnr + {round(coeff[1],2)}',fontdict={'size':'10','color':'r'})
print(f"fratcal dimension is {coeff[0]}")
print(f"alpha is {a}")
print(f"error is {error}")
plt.show()