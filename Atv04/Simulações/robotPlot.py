import numpy as np
import matplotlib.pyplot as plt
def drawRobot(x,y,q,s, color):
    p=np.zeros(36).reshape(12,3)
    p[0,:]=[1,1/7,1/s]
    p[1,:]=[-3/7,1,1/s]
    p[2,:]=[-5/7,6/7,1/s]
    p[3,:]=[-5/7,5/7,1/s]
    p[4,:]=[-3/7,2/7,1/s]
    p[5,:]=[-3/7,0,1/s]
    p[6,:]=[-3/7,-2/7,1/s]
    p[7,:]=[-5/7,-5/7,1/s]
    p[8,:]=[-5/7,-6/7,1/s]
    p[9,:]=[-3/7,-1,1/s]
    p[10,:]=[1,-1/7,1/s]
    p[11,:]=[1,1/7,1/s]
    #
    p=s*p
    #
    r=np.zeros(6).reshape(3,2)
    r[0,:]=[np.cos(q),np.sin(q)]
    r[1,:]=[-np.sin(q),np.cos(q)]
    r[2,:]=[x,y]
    #
    p=np.dot(p,r)
    X=p[:,0]
    Y=p[:,1]
    plt.plot(X,Y, color)

def plotRobot(x,y,q,s,color, step=2):
    for i in range(0, len(x), step):
        drawRobot(x[i],y[i],q[i],s, color)