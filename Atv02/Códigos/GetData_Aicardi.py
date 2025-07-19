# coppeliaSim
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

import numpy as np
import pandas as pd

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
goal = sim.getObject('/Goal')

''' VETORES A SEREM EXPORTADOS'''
# Vetor de tempo
t = []

# Posição e orientação do robô
x, y, phi = [], [], []

# Posição do alvo
xg, yg = [], []

# Grandezas de erro
e, theta, alpha = [], [], []

#velocidade linear e angular do robô
v, w = [], []

''' PARÂMETROS DE CONTROLE '''
k = 1
h = 1
gamma = 0.1

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
        phi.append(oriR[2])

        # Posição do alvo na cena
        posG = sim.getObjectPosition(goal,-1)
        xg.append(posG[0])
        yg.append(posG[1])
        
        # Calculo das grandezas de erro
        e.append(np.sqrt((xg[-1]-x[-1])**2 + (yg[-1]-y[-1])**2))
        theta.append(np.arctan2(yg[-1]-y[-1], xg[-1]-x[-1]))
        alpha.append(theta[-1] - phi[-1])

        # Cálculo das velocidades
        v.append(gamma * np.cos(alpha[-1]) * e[-1])
        w.append(k * alpha[-1] - gamma * (np.cos(alpha[-1]) * np.sin(alpha[-1]) / alpha[-1]) * (alpha[-1] + h * theta[-1]))

        td = td + hd

    tc = timeit.default_timer() - ti

# Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)


#Concatenando os vetores em um dataframe
data = np.array([t, x, y, phi, xg, yg, e, theta, alpha, v, w]).T
data = pd.DataFrame(data, columns=['t', 'x', 'y', 'phi', 'xg', 'yg', 'e', 'theta', 'alpha', 'v', 'w'])
data.to_csv('Data_Cena_4_Aicardi.csv', index=False)

print('Simulation Ended!')