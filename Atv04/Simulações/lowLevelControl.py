from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np

# parâmetros do robô (Pioneer 3DX)
R = 195e-3/2   # raio da roda (m)
L = 381e-3   # distância entre rodas (m)
#gamma = 0.328
#kappa = 1.08
gamma = 0.3
kappa = 2.2

def lowLevelController(e, alpha):
    global gamma, kappa

    v = gamma * e * np.cos(alpha)
    w = kappa * alpha + gamma * np.cos(alpha) * np.sin(alpha)
    return v, w

def controlRobot(sim, left_motor, right_motor, v, w):
    global R, L

    v_r = (2*v + w*L) / (2*R)
    v_l = (2*v - w*L) / (2*R)
    sim.setJointTargetVelocity(left_motor, v_l)
    sim.setJointTargetVelocity(right_motor, v_r)
    return