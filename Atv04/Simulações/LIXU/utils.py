import numpy as np

def calculateErros(x_r, y_r, theta_r, x_g, y_g):
    # erro até o goal
    e = np.sqrt((x_g - x_r)**2 + (y_g - y_r)**2)
    alpha = np.arctan2(y_g - y_r, x_g - x_r) - theta_r
    alpha = np.arctan2(np.sin(alpha), np.cos(alpha))  # normalizar [-pi; pi]
    return e, alpha


def stopCondition(e):       
    if e < 0.1:
       print("Objetivo alcançado!") 
       return True
    return False


def get_ultrasonic_readings(sim, usensors, max_dist=1.0):
    distances = []
    for sensor in usensors:
        detectionState, detectedPoint = sim.readProximitySensor(sensor)[:2]
        if detectionState:
            dist = np.linalg.norm(detectedPoint)  # distância medida
        else:
            dist = max_dist  # valor default se não detecta nada
        distances.append(dist)
    return np.array(distances)

def groupSensors(sim, usensors, alpha, max_dist=1.0):
    sensorDists = get_ultrasonic_readings(sim, usensors, max_dist)

    if abs(alpha) <= np.pi/2:
        gruppedSensors = {
            'SW': min(sensorDists[13], sensorDists[14]),  # 14,15
            'WE': min(sensorDists[15], sensorDists[0]),   # 16,1
            'NW': min(sensorDists[1],  sensorDists[2]),   # 2,3
            'NO': min(sensorDists[3],  sensorDists[4]),   # 4,5
            'NE': min(sensorDists[5],  sensorDists[6]),   # 6,7
            'ES': min(sensorDists[7],  sensorDists[8]),   # 8,9
            'SE': min(sensorDists[9],  sensorDists[10]),  # 10,11
            'SO': min(sensorDists[11], sensorDists[12])   # 12,13
        }
    else:
        gruppedSensors = {
            'SW': min(sensorDists[5],  sensorDists[6]),   # 6,7
            'WE': min(sensorDists[7],  sensorDists[8]),   # 8,9
            'NW': min(sensorDists[9],  sensorDists[10]),  # 10,11
            'NO': min(sensorDists[11], sensorDists[12]),  # 12,13
            'NE': min(sensorDists[13], sensorDists[14]),  # 14,15
            'ES': min(sensorDists[15], sensorDists[0]),   # 16,1
            'SE': min(sensorDists[1],  sensorDists[2]),   # 2,3
            'SO': min(sensorDists[3],  sensorDists[4])    # 4,5
        }

    return gruppedSensors