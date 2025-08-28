# coppeliaSim
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wallPlot import drawWall

import timeit

''' CONFIGURAÇÕES INICIAIS '''

print('Starting simpleTest.py ...')

client = RemoteAPIClient()
sim = client.getObject('sim')

# When simulation is not running, ZMQ message handling could be a bit
# slow, since the idle loop runs at 8 Hz by default. So let's make
# sure that the idle loop runs at full speed for this program:
defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
sim.setInt32Param(sim.intparam_idle_fps, 0)

''' ROBÔ e ALVO '''
p3dx = sim.getObject('/Pioneer_p3dx')

''' ALVO '''
goal = sim.getObject('/Goal')
posG = sim.getObjectPosition(goal,-1)
xg = posG[0]
yg = posG[1]

''' PAREDES '''
walls = []

i = 0
while True:
    try:
        wall = sim.getObject(f'/80cmHighWall100cm[{i}]')
        wall_P = sim.getObjectPosition(wall,-1)
        wall_O = sim.getObjectOrientation(wall,-1)
        walls.append([wall_P[0], wall_P[1], wall_O[2]])
        i += 1
    except:
        break

''' VETORES A SEREM EXPORTADOS'''
# Vetor de tempo
t = []

# Posição do robô
x, y, theta = [], [], []

# Grandezas de erro
e, alpha = [], []

# Grandezas sub Goal
e_sg, alpha_sg = [], []

#velocidade linear e angular do robô
v, w = [], []

''' SIMULAÇÃO '''
hd=50e-3 # passo de tempo
tc=0
td=0

# Starting simulation
print('Simulation Started!')
sim.startSimulation()

ti = timeit.default_timer()

while (sim.getSimulationState() != sim.simulation_stopped):
    
    if (tc>td):
        t.append(tc)

        # Posição e orientação do robô na cena
        posR = sim.getObjectPosition(p3dx,-1)
        oriR = sim.getObjectOrientation(p3dx,-1)
        x.append(posR[0])
        y.append(posR[1])
        theta.append(oriR[2])

        e.append(sim.getFloatSignal('e_error'))
        alpha.append(sim.getFloatSignal('alpha_error'))

        e_sg.append(sim.getFloatSignal('e_sg'))
        alpha_sg.append(sim.getFloatSignal('alpha_sg'))

        v.append(sim.getFloatSignal('v'))
        w.append(sim.getFloatSignal('omega'))

        td = td + hd

    tc = timeit.default_timer() - ti

# Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)

x = np.array(x)
y = np.array(y)
e_sg = np.array(e_sg)
alpha_sg = np.array(alpha_sg)


for wall in walls:
    drawWall(wall)
plt.plot(x, y)
plt.plot(x + e_sg * np.cos(alpha_sg), y + e_sg * np.sin(alpha_sg), 'ro')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Robot Path')
plt.grid()
plt.show()

#Concatenando os vetores em um dataframe
#data = np.array([t, x, y, theta, e, alpha, e_sg, alpha_sg, v, w, xg, yg, walls]).T
#data = pd.DataFrame(data, columns=['t', 'x', 'y', 'phi', 'xg', 'yg', 'e', 'theta', 'alpha', 'v', 'w'])
#data.to_csv('Data_Cena_4_Aicardi.csv', index=False)

print('Simulation Ended!')