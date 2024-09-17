from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
# TODO - parada quandoo não há melhoria na solução xbest a cada t iterações

#  O resultado do modelo (ótimo/subótimo encontrado), se dá pelo resultado
# mais frequentista da função de avalia¸c˜ao. Neste caso, como a fun¸c˜ao
# objetivo tem como contradom´ınio o conjunto dos
# reais (R) aproxime o resultado dos algoritmos de busca para trˆes casas
# decimais


class Algo:
    def __init__(self, x1, x2, max_it, qtd_stop, viz) -> None:
        self.x1 = x1
        self.x2 = x2
        self.max_it = max_it
        self.qtd_stop = qtd_stop
        self.viz = viz

    def hill_climbing(self, pertubation, function, find_max=True):
        '''
            Hill Climbing algorithm
        '''
        # Gerando resultado ótimo com base nos limites inferiores
        x1_opt, x2_opt = min(self.x1), min(self.x2)
        f_opt = function(x1_opt, x2_opt)
        it = 0
        it_s_melhoria = 0
        upgrade = True

        # Melhor resultado atual
        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}

        while it < self.max_it and upgrade and it_s_melhoria < self.qtd_stop:
            upgrade = False
            for _ in range(self.viz):

                # Gerando candidato
                x1_cand = pertubation(
                    x1_opt, min(self.x1), max(self.x1))
                x2_cand = pertubation(
                    x2_opt, min(self.x2), max(self.x2))
                f_cand = function(x1_cand, x2_cand)

                if find_max:
                    if f_cand > f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        upgrade = True
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        it_s_melhoria = 0
                        break
                    else:
                        it_s_melhoria += 1
                else:
                    if f_cand < f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        upgrade = True
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        it_s_melhoria = 0
                        break
                    else:
                        it_s_melhoria += 1

            it += 1
        best["F"] = round(best["F"], 3)
        return best

    def lrs(self, perturb, function, σ, find_max=True):
        '''
            Local Random Search algorithm
        '''
        # Definindo ótimo inicial
        x1_opt, x2_opt = (
            np.random.uniform(min(self.x1), max(self.x1)),
            np.random.uniform(min(self.x2), max(self.x2)),
        )
        f_opt = function(x1_opt, x2_opt)
        it = 0
        it_s_melhoria = 0
        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}

        # Perturbação do ótimo
        while it < self.max_it and it_s_melhoria < self.qtd_stop:
            for _ in range(self.viz):
                x1_cand = perturb(x1_opt, σ)
                x2_cand = perturb(x2_opt, σ)
                if min(self.x1) < x1_cand < max(self.x1) and (
                        min(self.x2) < x2_cand < max(self.x2)):
                    f_cand = function(x1_cand, x2_cand)
                    if find_max:
                        if f_cand > f_opt:
                            x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                            best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                            it_s_melhoria = 0
                            break
                        else:
                            it_s_melhoria += 1
                    else:
                        if f_cand < f_opt:
                            x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                            best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                            it_s_melhoria = 0
                            break
                        else:
                            it_s_melhoria += 1
            it += 1
        best["F"] = round(best["F"], 3)
        return best

    def grs(self, perturb, function, find_max=True):
        '''
            Global Random Search algorithm
        '''
        # Definindo ótimo inicial
        x1_opt, x2_opt, f_opt = (
            None, None, float('-inf') if find_max else float('inf')
        )

        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
        # Perturbação do ótimo
        i = 0
        it_s_melhoria = 0
        while i < self.max_it and it_s_melhoria < self.qtd_stop:
            x1_cand = perturb(min(self.x1), max(self.x1))
            x2_cand = perturb(min(self.x2), max(self.x2))

            if min(self.x1) < x1_cand < max(self.x1) and (
                    min(self.x2) < x2_cand < max(self.x2)):
                f_cand = function(x1_cand, x2_cand)
                if find_max:
                    if f_cand > f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        it_s_melhoria = 0
                    else:
                        it_s_melhoria += 1
                else:
                    if f_cand < f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        it_s_melhoria = 0
                    else:
                        it_s_melhoria += 1
            i += 1
        best["F"] = round(best["F"], 3)
        return best


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Supondo que você já tenha X, Y e func definidos.
    # Exemplo:
    X = np.linspace(-5, 5, 100)
    Y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X, Y)
    def func(x, y): return x**2 + y**2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotando a superfície
    ax.plot_surface(X, Y, func(X, Y), cmap='inferno')

    # Adicionando pontos 3D
    # Exemplo de pontos 3D
    x_points = np.array([1, 2, 3])
    y_points = np.array([1, 2, 3])
    z_points = func(x_points, y_points)

    ax.scatter(x_points, y_points, z_points, color='red', s=50, label='Pontos')

    # Adicionando título e rótulos
    ax.set_title(r'$f(x_1, x_2) = x_1^2+x_2^2$', fontsize=9)
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.set_zlabel(r'$f(x_1, x_2)$')

    # Adicionando contornos
    ax.contour(X, Y, func(X, Y), offset=-0.3, cmap='grey')

    # Adicionando a legenda
    ax.legend()

    plt.show()
