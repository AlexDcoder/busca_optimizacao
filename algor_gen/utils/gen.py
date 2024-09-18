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

        # Hiperparâmetros
        self.N = N
        self.p = p
        self.nd = nd
        self.lims = [lim_inf, lim_sup]
        self.recomb = recomb
        self.is_can = is_can
        self.qtd_geracoes = qtd_geracoes
        self.tam_torneio = tam_torneio
        self.population = self.generate_population()

    # Função a ser minimizada
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
        # Return a list of decoded values
        return [self.lims[0] + (self.lims[1]-self.lims[0])/(2**len(x)-1)*s]

    # Funções de Geração
    def generate_population(self):
        if self.is_can:
            return np.random.uniform(
                low=0, high=2, size=(self.N, self.p*self.nd)).astype(int)
        return np.random.uniform(
            low=self.lims[0], high=self.lims[1], size=(self.N, self.p))

    def generate_x(self):
        if self.is_can:
            return np.random.uniform(
                0, 2, self.p*self.nd).astype(int)
        return np.random.uniform(
            self.lims[0], self.lims[1], self.p)

    # Funções de Seleção
    def roleta(self, prob):
        i = 0
        s = prob[i]
        r = np.random.uniform()
        while s < r:
            i += 1
            s += prob[i]
        return self.population[i]

    def torneio(self):
        if self.tam_torneio <= 0 or self.tam_torneio > self.N:
            raise ValueError(
                "O tamanho do torneio deve ser maior que 0 e menor ou igual ao tamanho da população.")

        # Seleção dos lutadores
        index_fighters = np.random.choice(
            self.N, size=self.tam_torneio, replace=False)
        fighters = self.population[index_fighters]

        # Avaliação dos lutadores
        pontuation = [self.psi(fighter) for fighter in fighters]

        if not pontuation:
            raise ValueError("A lista de pontuação está vazia.")

        # Seleção do melhor lutador
        min_pontuation = min(pontuation)
        return fighters[pontuation.index(min_pontuation)]

    # Função de Recombinação
    def recombination(self, x1, x2):
        if self.is_can:
            # Por ponto de corte
            f1 = np.copy(x1)
            f2 = np.copy(x2)
            m = np.zeros(len(x1))
            idx = np.random.randint(1, len(m))
            m[idx:] = 1
            f1[m[:] == 1] = x2[m[:] == 1]
            f2[m[:] == 1] = x1[m[:] == 1]
            return f1, f2
        else:
            # SBX (Simulated Binary Crossover)
            eta = 1  # pode ajustar o parâmetro SBX
            u = np.random.rand(len(x1))
            beta = np.where(u <= 0.5, (2*u)**(1/(eta+1)),
                            (1/(2*(1-u)))**(1/(eta+1)))
            f1 = 0.5*((1 + beta)*x1 + (1 - beta)*x2)
            f2 = 0.5*((1 - beta)*x1 + (1 + beta)*x2)
            return f1, f2

    # Função de Mutação
    def mutation(self, x, tax_mutation):
        if self.is_can:
            # Mutação de um ponto
            idx = np.random.randint(0, len(x))
            x[idx] = 1 - x[idx]
            return x
        else:
            # Mutação Gaussiana
            return x + np.random.normal(0, 0.1, len(x))

    # Função de Execução
    def execute(self):
        # Armazenar os resultados de cada geração
        gen_results = []

        for ger in range(self.qtd_geracoes):
            nova_pop = []
            for i in range(self.N//2):
                # Seleção
                if self.is_can:
                    prob = np.array([self.psi(ind) for ind in self.population])
                    prob = prob / prob.sum()
                    parent1 = self.roleta(prob)
                    parent2 = self.roleta(prob)
                else:
                    parent1 = self.torneio()
                    parent2 = self.torneio()

                # Recombinação
                if np.random.rand() < self.recomb:
                    child1, child2 = self.recombination(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                # Mutação
                if np.random.rand() < 0.05:
                    child1 = self.mutation(child1, 0.05)
                if np.random.rand() < 0.05:
                    child2 = self.mutation(child2, 0.05)

                nova_pop.append(child1)
                nova_pop.append(child2)

            self.population = np.array(nova_pop)

            # Avaliar a população a cada geração
            best_values = [self.psi(ind) for ind in self.population]
            gen_results.append((ger, min(best_values), max(
                best_values), np.mean(best_values), np.std(best_values)))

        return gen_results
