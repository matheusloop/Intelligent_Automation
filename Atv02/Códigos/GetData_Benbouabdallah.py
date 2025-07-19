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
x, y, theta = [], [], []

# Posição do alvo
xg, yg = [], []

# Grandezas de erro
D, eD, phi, alpha = [], [], [], []

#velocidade linear e angular do robô
v, w = [], []

''' PARÂMETROS DE CONTROLE '''
Kv = 0.1
Kw = 1

''' SIMULAÇÃO '''
Dd = 0.001

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

        # Posição do alvo na cena
        posG = sim.getObjectPosition(goal,-1)
        xg.append(posG[0])
        yg.append(posG[1])
        
        # Calculo das grandezas de erro
        D.append(np.sqrt((xg[-1]-x[-1])**2 + (yg[-1]-y[-1])**2))
        eD.append(Dd - D[-1])
        phi.append(np.arctan2(yg[-1]-y[-1], xg[-1]-x[-1]))
        alpha.append(theta[-1] - phi[-1])

        # Cálculo das velocidades
        v.append(-Kv * eD[-1] * np.cos(alpha[-1]))
        w.append(-Kw * alpha[-1] - (v[-1]/D[-1])*np.sin(alpha[-1]))

        td = td + hd

    tc = timeit.default_timer() - ti

# Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)


#Concatenando os vetores em um dataframe
data = np.array([t, x, y, theta, xg, yg, D, eD, phi, alpha, v, w]).T
data = pd.DataFrame(data, columns=['t', 'x', 'y', 'theta', 'xg', 'yg', 'D', 'eD', 'phi', 'alpha', 'v', 'w'])
data.to_csv('Data_Cena_4_Benbouabdallah.csv', index=False)

print('Simulation Ended!')