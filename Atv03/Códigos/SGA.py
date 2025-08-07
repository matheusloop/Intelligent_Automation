import random
import numpy as np
import matplotlib.pyplot as plt
from numpy import arange, floor, ones, remainder, std, transpose, vstack, zeros
from numpy.random import rand, randn


def evolve(fitnessFunction, length, popSize, maxGens, probMutation,
           probCrossover=1, sigmaScaling=True, sigmaScalingCoeff=1,
           SUS=True, verbose=False):
    """
    Executa um algoritmo genético simples com operadores de seleção, crossover e mutação.
    Retorna o melhor indivíduo encontrado durante a evolução.
    Também exibe um gráfico da evolução do fitness médio e máximo por geração.
    """

    # Criação de máscaras reutilizáveis para crossover e mutação
    maskReposFactor = 5
    uniformCrossoverMaskRepos = rand(int(popSize / 2), (length + 1) * maskReposFactor) < 0.5
    mutMaskRepos = rand(popSize, (length + 1) * maskReposFactor) < probMutation

    # Histórico de fitness médio e máximo
    avgFitnessHist = zeros(maxGens)
    maxFitnessHist = zeros(maxGens)

    # Inicialização da população
    pop = zeros((popSize, length), dtype='int8')
    pop[rand(popSize, length) < 0.5] = 1

    # Variáveis para armazenar o melhor indivíduo
    bestFitnessEver = -np.inf
    bestIndividual = None

    for gen in range(maxGens):
        # Avaliação da aptidão
        fitnessVals = fitnessFunction(pop)
        fitnessVals = transpose(fitnessVals)
        maxFitnessHist[gen] = fitnessVals.max()
        avgFitnessHist[gen] = fitnessVals.mean()

        if verbose:
            print(f"gen = {gen:03d}   avgFitness = {avgFitnessHist[gen]:.3f}  maxFitness = {maxFitnessHist[gen]:.3f}")

        # Verifica se é o melhor indivíduo até agora
        currentBestIdx = np.argmax(fitnessVals)
        if fitnessVals[currentBestIdx] > bestFitnessEver:
            bestFitnessEver = fitnessVals[currentBestIdx]
            bestIndividual = pop[currentBestIdx].copy()

        # Escalonamento sigma
        if sigmaScaling:
            sigma = std(fitnessVals)
            if sigma:
                fitnessVals = 1 + (fitnessVals - fitnessVals.mean()) / (sigmaScalingCoeff * sigma)
                fitnessVals[fitnessVals < 0] = 0
            else:
                fitnessVals = ones((popSize,))

        # Cálculo da distribuição acumulada
        cumNormFitnessVals = np.cumsum(fitnessVals / fitnessVals.sum())
        
        # Seleção dos pais
        if SUS:
            markers = random.random() + arange(popSize, dtype='float') / popSize
            markers[markers > 1] -= 1
        else:
            markers = rand(popSize)
        markers = np.sort(markers)

        parentIndices = zeros(popSize, dtype='int16')
        ctr = 0
        for idx in range(popSize):
            while markers[idx] > cumNormFitnessVals[ctr]:
                ctr += 1
            parentIndices[idx] = ctr

        # Embaralhamento dos pais e crossover
        random.shuffle(parentIndices)
        firstParents = pop[parentIndices[:int(popSize / 2)], :]
        secondParents = pop[parentIndices[int(popSize / 2):], :]

        max_start = uniformCrossoverMaskRepos.shape[1] - length
        temp = random.randint(0, max_start)
        masks = uniformCrossoverMaskRepos[:, temp:temp + length]
        reprodIndices = rand(int(popSize / 2)) < 1 - probCrossover
        masks[reprodIndices, :] = False

        firstKids = firstParents.copy()
        secondKids = secondParents.copy()
        firstKids[masks] = secondParents[masks]
        secondKids[masks] = firstParents[masks]

        pop = vstack((firstKids, secondKids))

        # Mutação
        max_start = mutMaskRepos.shape[1] - length
        temp = random.randint(0, max_start)
        masks = mutMaskRepos[:, temp:temp + length]
        pop[masks] += 1
        pop = remainder(pop, 2)

    # === Mostra gráfico ao final da execução ===
    plt.plot(avgFitnessHist, label='Fitness Médio')
    plt.plot(maxFitnessHist, label='Fitness Máximo')
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.title('Evolução do Fitness por Geração')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return bestIndividual