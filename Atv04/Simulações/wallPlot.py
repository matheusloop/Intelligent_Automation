import matplotlib.pyplot as plt
import numpy as np

def drawWall(wall):
    if np.abs(wall[2]) >= np.pi/4:
        plt.plot([wall[0]-0.5, wall[0]+0.5], [wall[1]+0.075, wall[1]+0.075], 'k-')
        plt.plot([wall[0]-0.5, wall[0]+0.5], [wall[1]-0.075, wall[1]-0.075], 'k-')
        plt.plot([wall[0]-0.5, wall[0]-0.5], [wall[1]-0.075, wall[1]+0.075], 'k-')
        plt.plot([wall[0]+0.5, wall[0]+0.5], [wall[1]-0.075, wall[1]+0.075], 'k-')
    else:
        plt.plot([wall[0]-0.075, wall[0]+0.075], [wall[1]-0.5, wall[1]-0.5], 'k-')
        plt.plot([wall[0]-0.075, wall[0]+0.075], [wall[1]+0.5, wall[1]+0.5], 'k-')
        plt.plot([wall[0]-0.075, wall[0]-0.075], [wall[1]-0.5, wall[1]+0.5], 'k-')
        plt.plot([wall[0]+0.075, wall[0]+0.075], [wall[1]-0.5, wall[1]+0.5], 'k-')
