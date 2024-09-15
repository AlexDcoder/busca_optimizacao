import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from utils.problem_solver import Algo


def func(x1, x2):
    return x1 * np.sin(4*np.pi*x1) - x2 * np.sin(4*np.pi*x2) + 1

# Pertubação para o Hill Climbing


def perturb(x, lower_bound, upper_bound, e=math.pow(10, -2)):
    cand = np.random.uniform(low=x-e, high=x+e)
    return np.clip(cand, lower_bound, upper_bound)

# Pertubação para o Local Random Search


def perturb2(x, σ):
    n = round(np.random.uniform(0, σ), 3)
    return x + n

# Pertubação para o Global Random Search


def perturb3(min, max):
    return round(np.random.uniform(min, max), 3)


x1_axis = np.linspace(-1, 3)
x2_axis = np.linspace(-1, 3)

fig = plt.figure(0)

# Criando base para o gráfico
X, Y = np.meshgrid(x1_axis, x2_axis)
fig = plt.figure(1)
ax = fig.add_subplot(projection='3d')

# Instanciando o resolvedor do problema
algo = Algo(x1_axis, x2_axis, 10000, 100, 20)
hc_results = []
lrs_results = []
grs_results = []

# Executando o Algoritmo por R vezes
for i in range(100):
    # Resultados do Hill Climbing
    hc_results.append(algo.hill_climbing(perturb, func, False))
    ax.scatter(
        hc_results[i]["X1"], hc_results[i]
        ["X2"], hc_results[i]["F"], marker='o', c='r')

    # Resultados do Local Random Search
    lrs_results.append(algo.lrs(perturb2, func, 0.5, False))
    ax.scatter(
        lrs_results[i]["X1"], lrs_results[i]
        ["X2"], lrs_results[i]["F"], marker='X', color='b')

    # Resultados do Global Random Search
    grs_results.append(algo.grs(perturb2, func, False))
    ax.scatter(
        grs_results[i]["X1"], grs_results[i]
        ["X2"], grs_results[i]["F"], marker='o', c='green')

# Gráfico geral
ax.plot_surface(X, Y, func(X, Y), cmap='jet')
ax.contour(X, Y, func(X, Y), offset=-0.3, cmap='grey')
plt.show()

g = gs.GridSpec(3, 3)
ax1 = plt.subplot(g[0, :])
ax2 = plt.subplot(g[1, :])
ax3 = plt.subplot(g[2, :])

# Plotando os histogramas com legendas para os diferentes datasets
v1, v2 = (
    ax1.hist(
        [r["X1"] for r in hc_results], bins=100,
        alpha=0.5, label='X1', color='blue'),
    ax1.hist(
        [r["X2"] for r in hc_results], bins=100,
        alpha=0.5, label='X2', color='orange'))

ax1.set_title('Histograma para HC Results')
ax1.set_xlabel('Valor')
ax1.set_ylabel('Frequência')
ax1.legend()

indexes_v1 = np.where(v1[0] == v1[0].max())
indexes_v2 = np.where(v2[0] == v2[0].max())
print(v1[1][indexes_v1])
print(v2[1][indexes_v2])

v1, v2 = (
    ax2.hist(
        [r["X1"] for r in lrs_results], bins=100,
        alpha=0.5, label='X1', color='green'),
    ax2.hist(
        [r["X2"] for r in lrs_results], bins=100,
        alpha=0.5, label='X2', color='red'))

ax2.set_title('Histograma para LRS Results')
ax2.set_xlabel('Valor')
ax2.set_ylabel('Frequência')
ax2.legend()

indexes_v1 = np.where(v1[0] == v1[0].max())
indexes_v2 = np.where(v2[0] == v2[0].max())
print(v1[1][indexes_v1])
print(v2[1][indexes_v2])

v1, v2 = (
    ax3.hist(
        [r["X1"] for r in grs_results], bins=100,
        alpha=0.5, label='X1', color='purple'),
    ax3.hist(
        [r["X2"] for r in grs_results], bins=100,
        alpha=0.5, label='X2', color='brown'))


ax3.set_title('Histograma para GRS Results')
ax3.set_xlabel('Valor')
ax3.set_ylabel('Frequência')
ax3.legend()

indexes_v1 = np.where(v1[0] == v1[0].max())
indexes_v2 = np.where(v2[0] == v2[0].max())
print(v1[1][indexes_v1])
print(v2[1][indexes_v2])

# Ajusta o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Mostra o gráfico
plt.show()
