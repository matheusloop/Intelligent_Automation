import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np

from fuzzy_init import *
from lowLevelControl import *
from highLevelControl import *
from utils import *

''' Inicializar simulação '''
sim = connect(port=23000)
left_motor, right_motor, robot, goal, usensors = get_handles(sim)

# iniciar simulação
sim.startSimulation()
print("Simulação iniciada em modo síncrono.")


''' Simulação em execução '''  
try:
    while True:
        # posição e orientação do robô
        x_r, y_r = np.array(sim.getObjectPosition(robot, -1))[:2]  # (x, y)
        theta_r = sim.getObjectOrientation(robot, -1)[2]           # (alpha, beta, gamma) = Euler XYZ
        x_g, y_g = np.array(sim.getObjectPosition(goal, -1))[:2]   # (x, y)

        e, alpha = calculateErros(x_r, y_r, theta_r, x_g, y_g)
        if stopCondition(e): break

        # leituras dos sensores ultrassônicos
        groupped_sensors = groupSensors(sim, usensors, np.pi/4)
        
        #for k, v in grouped_sensors.items():
        #    print(f"{k}={v:.2f}", end=" | ")
        # controlador Lyapunov


        #e_gs, alpha_gs = goalSeeking(e, alpha)

        e, alpha = obstacleAvoidance(groupped_sensors, alpha)

        print(f'e = {e:.2f} | alpha = {180*alpha/np.pi:.2f}')
        #print(f'e={e:.2f}, alpha={180*alpha/np.pi:.2f}, oa={oa}')
        v, w = lowLevelController(e, alpha)
        # converter para velocidades de roda
        controlRobot(sim ,left_motor, right_motor, v, w)
        #time.sleep(1)
        sim.step()

finally:
    sim.stopSimulation()
    print("Simulação encerrada.")
