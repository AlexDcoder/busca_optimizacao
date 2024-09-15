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
        print("HC")
        # Gerando resultado ótimo com base nos limites inferiores
        x1_opt, x2_opt = round(min(self.x1), 3), round(min(self.x2), 3)
        f_opt = round(function(x1_opt, x2_opt), 3)
        it = 0
        it_s_melhoria = 0
        upgrade = True

        # Melhor resultado atual
        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
        print(f"{best}")

        while it < self.max_it and upgrade and it_s_melhoria < self.qtd_stop:
            upgrade = False
            for _ in range(self.viz):

                # Gerando candidato
                x1_cand = round(pertubation(
                    x1_opt, min(self.x1), max(self.x1)), 3)
                x2_cand = round(pertubation(
                    x2_opt, min(self.x2), max(self.x2)), 3)
                f_cand = round(function(x1_cand, x2_cand), 3)

                if min(self.x1) < x1_cand < max(self.x1) and (
                        min(self.x2) < x2_cand < max(self.x2)):
                    if find_max:
                        if f_cand > f_opt:
                            x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                            upgrade = True
                            best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                            break
                        else:
                            it_s_melhoria += 1
                    else:
                        if f_cand < f_opt:
                            x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                            upgrade = True
                            best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                            break
                        else:
                            it_s_melhoria += 1
                else:
                    it_s_melhoria += 1

            it += 1
        return best

    def lrs(self, perturb, function, σ, find_max=True):
        '''
            Local Random Search algorithm
        '''
        print("LRS")
        # Definindo ótimo inicial
        x1_opt, x2_opt = (
            round(np.random.uniform(min(self.x1), max(self.x1)), 3),
            round(np.random.uniform(min(self.x2), max(self.x2)), 3),
        )
        f_opt = function(x1_opt, x2_opt)
        it = 0
        it_s_melhoria = 0
        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
        print(f"{best}")

        # Perturbação do ótimo
        while it < self.max_it and it_s_melhoria < self.qtd_stop:
            x1_cand = perturb(x1_opt, σ)
            x2_cand = perturb(x2_opt, σ)
            if min(self.x1) < x1_cand < max(self.x1) and (
                    min(self.x2) < x2_cand < max(self.x2)):
                f_cand = function(x1_cand, x2_cand)
                if find_max:
                    if f_cand > f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        break
                    else:
                        it_s_melhoria += 1
                else:
                    if f_cand < f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        break
                    else:
                        it_s_melhoria += 1
            it += 1
        return best

    def grs(self, perturb, function, find_max=True):
        '''
            Global Random Search algorithm
        '''
        print("GRS")
        # Definindo ótimo inicial
        x1_opt, x2_opt = (
            round(np.random.uniform(min(self.x1), max(self.x1)), 3),
            round(np.random.uniform(min(self.x2), max(self.x2)), 3),
        )
        f_opt = round(function(x1_opt, x2_opt), 3)
        i = 0
        it_s_melhoria = 0
        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
        print(f"{best}")
        # Perturbação do ótimo
        while i < self.max_it:
            x1_cand = round(perturb(min(self.x1), max(self.x1)), 3)
            x2_cand = round(perturb(min(self.x2), max(self.x2)), 3)
            if min(self.x1) < x1_cand < max(self.x1) and (
                    min(self.x2) < x2_cand < max(self.x2)):
                f_cand = round(function(x1_cand, x2_cand), 3)
                if find_max:
                    if f_cand > f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        break
                    else:
                        it_s_melhoria += 1
                else:
                    if f_cand < f_opt:
                        x1_opt, x2_opt, f_opt = x1_cand, x2_cand, f_cand
                        best = {"X1": x1_opt, "X2": x2_opt, "F": f_opt}
                        break
                    else:
                        it_s_melhoria += 1
            i += 1
        return best


if __name__ == '__main__':
    print(round(1.008, 3))
