# coppeliaSim
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
# coppeliaSim

import timeit, numpy, scipy
import matplotlib.pyplot as plt
#
def drawRobot(x,y,q,s,h):
    p=numpy.zeros(36).reshape(12,3)
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
    r=numpy.zeros(6).reshape(3,2)
    r[0,:]=[numpy.cos(q),numpy.sin(q)]
    r[1,:]=[-numpy.sin(q),numpy.cos(q)]
    r[2,:]=[x,y]
    #
    p=numpy.dot(p,r)
    X=p[:,0]
    Y=p[:,1]
    h.plot(X,Y,'r-')
#
print('Starting simpleTest.py ...')
#
client = RemoteAPIClient()
sim = client.getObject('sim')

# When simulation is not running, ZMQ message handling could be a bit
# slow, since the idle loop runs at 8 Hz by default. So let's make
# sure that the idle loop runs at full speed for this program:
defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
sim.setInt32Param(sim.intparam_idle_fps, 0)

objectName='/PioneerP3DX'
objectHandle=sim.getObject(objectName)
#
objectPosition=sim.getObjectPosition(objectHandle,-1)
objectOrientation=sim.getObjectOrientation(objectHandle,-1)
objectQuaternion=sim.getObjectQuaternion(objectHandle,-1)
#
np=100
hd=50e-3
tf=np*hd
kd=0
tc=0
td=0
ta=numpy.zeros(np)
xp=numpy.zeros(np)
yp=numpy.zeros(np)
fp=numpy.zeros(np)
#
# Staring simulation
sim.startSimulation()
#
ti=timeit.default_timer()
#
while (tc<tf):
    #
    if (tc>td):
     ta[kd]=tc
     objectPosition=sim.getObjectPosition(objectHandle,-1)
     objectOrientation=sim.getObjectOrientation(objectHandle,-1)
     objectQuaternion=sim.getObjectQuaternion(objectHandle,-1)
     #
     xp[kd]=objectPosition[0]
     yp[kd]=objectPosition[1]
     fp[kd]=objectOrientation[2]
     #
     td=td+hd
     kd=kd+1
    #
    tc=timeit.default_timer()-ti
#
sim.stopSimulation()
# If you need to make sure we really stopped:
while sim.getSimulationState() != sim.simulation_stopped:
    time.sleep(0.1)

# Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)
#
fig,ax=plt.subplots()
ax.axis('equal')
ax.plot(xp,yp,color='blue',linestyle='dashed',linewidth=1)
plt.grid()
plt.title("Top view: robot trajectory")
plt.xlabel("x, m")
plt.ylabel("y, m")
plt.show(block=False)
#
for i in range(0,len(xp)-1,int(round(len(xp)/20))):
    drawRobot(xp[i],yp[i],fp[i],0.01,ax)
#
plt.show()
