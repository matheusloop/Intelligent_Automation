import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

''' FUZIFICAÇÃO '''
# Função que retorna os vetores de pertinência
def sensorFuzzification(sensorLabel):
    fuzzyLabel = ctrl.Antecedent(np.arange(0, 1.003, 0.003), sensorLabel)

    fuzzyLabel['N'] = np.where(fuzzyLabel.universe <= 0.25, 1, fuzz.gaussmf(fuzzyLabel.universe, 0.25, 0.08))
    fuzzyLabel['M'] = fuzz.gaussmf(fuzzyLabel.universe, 0.5, 0.08)
    fuzzyLabel['F'] = np.where(fuzzyLabel.universe >= 0.75, 1, fuzz.gaussmf(fuzzyLabel.universe, 0.75, 0.08))

    return fuzzyLabel


def orientationFuzzification(orientationLabel):
    fuzzyLabel = ctrl.Antecedent(np.arange(-np.pi, np.pi+0.01, 0.01), orientationLabel)

    for i, label in enumerate(['SOn', 'SE', 'ES', 'NE', 'NO', 'NW', 'WE', 'SW', 'SOp']):
        fuzzyLabel[label] = fuzz.gaussmf(fuzzyLabel.universe, -np.pi + i*np.pi/4, 0.33)

    return fuzzyLabel

''' DESFUZIFICAÇÃO '''
def positionDesfuzzification(positionLabel):
    fuzzyLabel = ctrl.Consequent(np.arange(0, 4.01, 0.01), positionLabel)

    sigma = 0.85
    fuzzyLabel['N'] = fuzz.gaussmf(fuzzyLabel.universe, 0, sigma)
    fuzzyLabel['M'] = fuzz.gaussmf(fuzzyLabel.universe, 2, sigma)
    fuzzyLabel['F'] = fuzz.gaussmf(fuzzyLabel.universe, 4, sigma)

    return fuzzyLabel

def orientationDesfuzzification(orientationLabel):
    fuzzyLabel = ctrl.Consequent(np.arange(-np.pi, np.pi+0.01, 0.01), orientationLabel)

    for i, label in enumerate(['SOn', 'SE', 'ES', 'NE', 'NO', 'NW', 'WE', 'SW', 'SOp']):
        fuzzyLabel[label] = fuzz.gaussmf(fuzzyLabel.universe, -np.pi + i*np.pi/4, 0.33)

    return fuzzyLabel