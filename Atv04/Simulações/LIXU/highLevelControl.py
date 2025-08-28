from fuzzyDesfuzzyfication import *

def goalSeeking(e, alpha):
    return e, alpha

def obstacleAvoidance(groupped_sensors, alpha):
    ES_input = sensorFuzzification('ES_input')
    NE_input = sensorFuzzification('NE_input')
    NO_input = sensorFuzzification('NO_input')
    NW_input = sensorFuzzification('NW_input')
    WE_input = sensorFuzzification('WE_input')
    alpha_input = orientationFuzzification('alpha_input')

    e_output     = positionDesfuzzification('e_output')
    alpha_output = orientationDesfuzzification('alpha_output')

    rules = []

    rules.append(ctrl.Rule(NO_input['F'],      e_output['F']))
    rules.append(ctrl.Rule(NO_input['F'], alpha_output['NO']))

    rules.append(ctrl.Rule(NO_input['M'],      e_output['M']))
    rules.append(ctrl.Rule(NO_input['M'], alpha_output['NO']))

    rules.append(ctrl.Rule(NO_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NO_input['N'], alpha_output['NO']))

    rules.append(ctrl.Rule(NO_input['N'] & (NE_input['M'] | NE_input['N']),      e_output['N']))
    rules.append(ctrl.Rule(NO_input['N'] & (NE_input['M'] | NE_input['N']), alpha_output['WE']))

    rules.append(ctrl.Rule(NO_input['N'] & (NW_input['M'] | NW_input['N']),      e_output['N']))
    rules.append(ctrl.Rule(NO_input['N'] & (NW_input['M'] | NW_input['N']), alpha_output['ES']))

    rules.append(ctrl.Rule(NO_input['N'] & (ES_input['M'] | ES_input['N']),      e_output['N']))
    rules.append(ctrl.Rule(NO_input['N'] & (ES_input['M'] | ES_input['N']), alpha_output['WE']))

    rules.append(ctrl.Rule(NO_input['N'] & (WE_input['M'] | WE_input['N']),      e_output['N']))
    rules.append(ctrl.Rule(NO_input['N'] & (WE_input['M'] | WE_input['N']), alpha_output['ES']))

    system = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(system)

    simulation.input['WE_input']    = groupped_sensors['WE']
    simulation.input['NW_input']    = groupped_sensors['NW']
    simulation.input['NO_input']    = groupped_sensors['NO']
    simulation.input['NE_input']    = groupped_sensors['NE']
    simulation.input['ES_input']    = groupped_sensors['ES']
    #simulation.input['alpha_input'] = alpha

    simulation.compute()

    return simulation.output['e_output'], simulation.output['alpha_output']





'''
rules.append(ctrl.Rule(WE_input['N'] & ES_input['N'] & alpha_input['NO'],  e_output['N']))
    rules.append(ctrl.Rule(WE_input['N'] & ES_input['N'] & alpha_input['NO'],  e_output['F']))

    #Case 1
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['N'], alpha_output['NO']))

    #Case 2
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['M'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['M'], alpha_output['NE']))

    #Case 3
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['F'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['N'] & NE_input['F'], alpha_output['NE']))

    #Case 4
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['N'], alpha_output['NO']))

    #Case 5
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['M'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['M'], alpha_output['NE']))

    #Case 6
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['F'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['M'] & NE_input['F'], alpha_output['NE']))

    #Case 7
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['N'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['N'], alpha_output['NO']))

    #Case 8
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['M'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['M'], alpha_output['ES']))

    #Case 9
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['F'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['N'] & NO_input['F'] & NE_input['F'], alpha_output['NE']))

    #Case 10
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['N'], alpha_output['WE']))

    #Case 11
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['M'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['M'], alpha_output['NO']))

    #Case 12
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['F'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['N'] & NE_input['F'], alpha_output['ES']))

    #Case 13
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['N'], alpha_output['WE']))

    #Case 14
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['M'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['M'], alpha_output['NO']))

    #Case 15
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['F'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['M'] & NE_input['F'], alpha_output['NE']))

    #Case 16
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['N'], alpha_output['WE']))

    #Case 17
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['M'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['M'], alpha_output['NO']))

    #Case 18
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['F'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['M'] & NO_input['F'] & NE_input['F'], alpha_output['NE']))

    #Case 19
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['N'], alpha_output['WE']))

    #Case 20
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['M'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['M'], alpha_output['NW']))

    #Case 21
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['F'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['N'] & NE_input['F'], alpha_output['WE']))

    #Case 22
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['N'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['N'], alpha_output['NO']))

    #Case 23
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['M'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['M'], alpha_output['NW']))

    #Case 24
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['F'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['M'] & NE_input['F'], alpha_output['NW']))

    #Case 25
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['N'],      e_output['N']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['N'], alpha_output['NW']))

    #Case 26
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['M'],      e_output['M']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['M'], alpha_output['NW']))

    #Case 27
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['F'],      e_output['F']))
    rules.append(ctrl.Rule(NW_input['F'] & NO_input['F'] & NE_input['F'], alpha_output['NO']))
'''