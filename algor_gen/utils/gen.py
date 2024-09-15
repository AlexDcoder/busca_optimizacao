import numpy as np


class AlgoGenCont:
    def __init__(
        self, A, p, nd, lim_inf, lim_sup, recomb, is_can=True,
            tam_torneio=0) -> None:
        self.A = A
        self.p = p
        self.nd = nd
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
        self.recomb = recomb
        self.is_can = is_can
        self.cromoss = self.repr_cromossom()
        self.tam_torneio = tam_torneio

    def f(self, x):
        # função de Rastringin
        if self.is_can:
            s = 0
            for i in range(len(x)):
                v = (2**i) * x[len(x)-i-1]
                s += v**2 - self.A * np.cos(2*np.pi*v)
            return self.A * self.p + s

        return self.A * self.p + sum([
            xi**2 - self.A * np.cos(2*np.pi*xi)
            for xi in x])

    def psi(self, x):
        # Função aptidão
        return self.f(x) + 1

    def roleta(self):
        dec_bin = [
            sum([2**i * c[len(c)-i-1] for i in range(len(c))])
            for c in self.cromoss]
        total = sum(dec_bin)
        probs = [dec / total for dec in dec_bin]
        i = 0
        s = probs[i]
        r = np.random.uniform()
        while s < r:
            i += 1
            s += probs[i]
        return self.cromoss[i, :]

    def torneio(self):
        sobrevivente = np.random.choice(
            len(self.cromoss), self.tam_torneio, replace=False)
        print(sobrevivente)
        return self.cromoss[sobrevivente]

    def recombination(self):
        pass

    def mutation(self):
        if self.is_can:
            return
        return

    def repr_cromossom(self):
        if self.is_can:
            return np.random.uniform(
                low=0, high=2,
                size=(self.A, self.p)).astype(int)
        return np.random.uniform(
            low=self.lim_inf,
            high=self.lim_sup, size=(self.A, self.p))

    def exec(self):
        if self.is_can:
            return
        return


class AlgoGenDisc:
    def __init__(self, N, np, qtd_max_geracoes):
        self.N = N
        self.qtd_max_geracoes = qtd_max_geracoes
        self.np = np
        self.mutations: dict[str, int] = {}
        self.cromossom = self.gerar_populacao()

    def gerar_populacao(self):
        return [
            np.random.uniform(low=0, high=self.N, size=(self.np)).astype(int)
            for _ in range(self.N)]

    def roleta(self):
        pass

    def elitismo(self):
        pass

    def recombination(self):
        pass

    def mutation(self):
        pass
