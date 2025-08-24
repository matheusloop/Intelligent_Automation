from coppeliasim_zmqremoteapi_client import RemoteAPIClient

def connect(port=23000):
    client = RemoteAPIClient(port=port)
    sim = client.getObject('sim')
    sim.setStepping(True)
    return sim

def get_handles(sim):
    left_motor = sim.getObject('/Pioneer_p3dx_leftMotor')
    right_motor = sim.getObject('/Pioneer_p3dx_rightMotor')
    robot = sim.getObject('/Pioneer_p3dx')
    goal = sim.getObject('/Goal')

    # criar coleção de obstáculos
    obstacles = sim.createCollection(0)

    # adiciona tudo
    sim.addItemToCollection(obstacles, sim.handle_all, -1, 0)

    # remove a árvore do próprio robô
    sim.addItemToCollection(obstacles, sim.handle_tree, robot, 1)

    # pega os 16 sensores e seta pra só detectarem a coleção de obstáculos
    usensors = []
    for i in range(1, 17):
        sensor = sim.getObject(f"/Pioneer_p3dx_ultrasonicSensor{i}")
        sim.setObjectInt32Param(sensor, sim.proxintparam_entity_to_detect, obstacles)
        usensors.append(sensor)

    return left_motor, right_motor, robot, goal, usensors