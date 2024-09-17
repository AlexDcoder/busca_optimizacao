import numpy as np


class AlgoGenCont:
    def __init__(
            self,
            N: int, p: int, nd: int,
            lim_inf: int | float, lim_sup: int | float,
            recomb: float,
            is_can=True,
            tam_torneio=0,
            qtd_geracoes: int = 10) -> None:
        # Hiperparâmtros
        self.N = N
        self.p = p
        self.nd = nd
        self.lims = [lim_inf, lim_sup]
        self.recomb = recomb
        self.is_can = is_can
        self.qtd_geracoes = qtd_geracoes
        self.tam_torneio = tam_torneio

        self.population = self.generate_population()
        self.probabilities: list = self.defining_probs()

    def rastrigin(self, x):
        if self.is_can:
            decod_x = self.phi(x)
            return 10*self.p + sum([i**2 - 10*np.cos(2*np.pi*i) for i in decod_x])
        else:
            return 10*self.p + sum([i**2 - 10*np.cos(2*np.pi*i) for i in x])

    def psi(self, x):
        return self.rastrigin(x) + 1

    def phi(self, x):
        s = 0
        for i in range(len(x)):
            s += x[len(x)-i-1]*2**i
        return self.lims[0] + (self.lims[1]-self.lims[0])/(2**len(x)-1)*s

    def generate_population(self):
        if self.is_can:
            return np.random.uniform(
                low=0, high=2, size=(self.N, self.p*self.nd)).astype(int)
        return np.random.uniform(
            low=self.lims[0], high=self.lims[1], size=(self.N, self.p))

    # Definindo a probabilidade de cada
    def defining_probs(self):
        probs = []
        for i in self.population:
            if self.is_can:
                pass
            else:
                pass

        return probs

    # Algoritmos de seleção
    def roleta(self, prob):
        i = 0
        s = prob[i]
        r = np.random.uniform()
        while s < r:
            i += 1
            s += prob[i]
        return prob[i, :]

    def torneio(self):
        index_fighters = np.random.choice(
            self.N, size=self.tam_torneio, replace=False)
        fighters = self.population[index_fighters]
        pontuation = [self.psi(fighter) for fighter in fighters]
        return fighters[pontuation.index(min(pontuation))]

    def recombination(self):
        if self.is_can:
            return
        else:
            return

    def mutation(self):
        if self.is_can:
            # Mutação de  um só ponto
            return
        else:
            # Mutação Gaussiana
            return

    def execute(self):
        for ger in range(self.qtd_geracoes):
            if self.is_can:
                return
            else:
                return
