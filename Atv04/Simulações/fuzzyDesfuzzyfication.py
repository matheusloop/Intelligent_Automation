import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

''' FUZIFICAÇÃO '''
# Função que retorna os vetores de pertinência
def sensorFuzzification(sensorLabel):
    fuzzyLabel = ctrl.Antecedent(np.arange(0, 1.03, 0.03), sensorLabel)

    fuzzyLabel['N'] = np.where(fuzzyLabel.universe <= 0.35, 1, fuzz.trimf(fuzzyLabel.universe, [0.35, 0.35, 0.55]))
    fuzzyLabel['M'] = fuzz.trimf(fuzzyLabel.universe, [0.35, 0.55, 0.75])
    fuzzyLabel['F'] = np.where(fuzzyLabel.universe >= 0.75, 1, fuzz.trimf(fuzzyLabel.universe, [0.55, 0.75, 0.75]))

    return fuzzyLabel


def orientationFuzzification(orientationLabel):
    fuzzyLabel = ctrl.Antecedent(np.arange(-np.pi, np.pi+0.1, 0.1), orientationLabel)

    fuzzyLabel['SOn'] = fuzz.trimf(fuzzyLabel.universe, [-np.pi+0*np.pi/4, -np.pi+0*np.pi/4, -np.pi+1*np.pi/4])
    fuzzyLabel['SE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+0*np.pi/4, -np.pi+1*np.pi/4, -np.pi+2*np.pi/4])
    fuzzyLabel['ES']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+1*np.pi/4, -np.pi+2*np.pi/4, -np.pi+3*np.pi/4])
    fuzzyLabel['NE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+2*np.pi/4, -np.pi+3*np.pi/4, -np.pi+4*np.pi/4])
    fuzzyLabel['NO']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+3*np.pi/4, -np.pi+4*np.pi/4, -np.pi+5*np.pi/4])
    fuzzyLabel['NW']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+4*np.pi/4, -np.pi+5*np.pi/4, -np.pi+6*np.pi/4])
    fuzzyLabel['WE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+5*np.pi/4, -np.pi+6*np.pi/4, -np.pi+7*np.pi/4])
    fuzzyLabel['SW']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+6*np.pi/4, -np.pi+7*np.pi/4, -np.pi+8*np.pi/4])
    fuzzyLabel['SOp'] = fuzz.trimf(fuzzyLabel.universe, [-np.pi+7*np.pi/4, -np.pi+8*np.pi/4, -np.pi+8*np.pi/4])

    return fuzzyLabel

''' DESFUZIFICAÇÃO '''
def positionDesfuzzification(positionLabel):
    fuzzyLabel = ctrl.Consequent(np.arange(0, 4.1, 0.1), positionLabel)

    sigma = 0.85
    fuzzyLabel['N'] = fuzz.trimf(fuzzyLabel.universe, [0, 0, 2])
    fuzzyLabel['M'] = fuzz.trimf(fuzzyLabel.universe, [0, 2, 4])
    fuzzyLabel['F'] = fuzz.trimf(fuzzyLabel.universe, [2, 4, 4])

    return fuzzyLabel

def orientationDesfuzzification(orientationLabel):
    fuzzyLabel = ctrl.Consequent(np.arange(-np.pi, np.pi+0.1, 0.1), orientationLabel)

    fuzzyLabel['SOn'] = fuzz.trimf(fuzzyLabel.universe, [-np.pi+0*np.pi/4, -np.pi+0*np.pi/4, -np.pi+1*np.pi/4])
    fuzzyLabel['SE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+0*np.pi/4, -np.pi+1*np.pi/4, -np.pi+2*np.pi/4])
    fuzzyLabel['ES']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+1*np.pi/4, -np.pi+2*np.pi/4, -np.pi+3*np.pi/4])
    fuzzyLabel['NE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+2*np.pi/4, -np.pi+3*np.pi/4, -np.pi+4*np.pi/4])
    fuzzyLabel['NO']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+3*np.pi/4, -np.pi+4*np.pi/4, -np.pi+5*np.pi/4])
    fuzzyLabel['NW']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+4*np.pi/4, -np.pi+5*np.pi/4, -np.pi+6*np.pi/4])
    fuzzyLabel['WE']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+5*np.pi/4, -np.pi+6*np.pi/4, -np.pi+7*np.pi/4])
    fuzzyLabel['SW']  = fuzz.trimf(fuzzyLabel.universe, [-np.pi+6*np.pi/4, -np.pi+7*np.pi/4, -np.pi+8*np.pi/4])
    fuzzyLabel['SOp'] = fuzz.trimf(fuzzyLabel.universe, [-np.pi+7*np.pi/4, -np.pi+8*np.pi/4, -np.pi+8*np.pi/4])

    return fuzzyLabel