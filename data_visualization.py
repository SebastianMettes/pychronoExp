import numpy as np
from matplotlib import pyplot as plt 


def data(path,stepsize):
    List = np.genfromtxt(path,delimiter=' ')
    zeros = np.zeros(shape = (List.shape[0],1))
    for i in range(0,len(zeros)):
        zeros[i] = i*stepsize
    List = np.concatenate((zeros,List),axis = 1)
    return(List)

data01 = data("/home/sebastian/code/pychronoExp/Results/11.05.2020/11.05.2020/11.16.2020/0.01platip2position.txt",0.01)
data005 = data("/home/sebastian/code/pychronoExp/Results/11.05.2020/11.05.2020/11.16.2020/0.005platip2position.txt",0.005)
data001 = data("/home/sebastian/code/pychronoExp/Results/11.05.2020/11.05.2020/11.16.2020/0.001platip2position.txt",0.001)
data0005 = data("/home/sebastian/code/pychronoExp/Results/11.05.2020/11.05.2020/11.16.2020/0.0005platip2position.txt",0.0005)
data0001 = data("/home/sebastian/code/pychronoExp/Results/11.05.2020/11.05.2020/11.16.2020/0.0001platip2position.txt",0.0001)

plt.plot(data01[0],data01[1],data005[0],data005[1],data001[0],data001[1],data0005[0],data0005[1],data0001[0],data0001[1])
