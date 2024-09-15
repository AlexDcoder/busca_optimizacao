import numpy as np
import matplotlib.pyplot as plt
import time

# Função que calcula o número de pares de rainhas se atacando


def num_pares_atacando(solucao):
    ataques = 0
    n = len(solucao)
    for i in range(n):
        for j in range(i + 1, n):
            if solucao[i] == solucao[j] or abs(solucao[i] - solucao[j]) == abs(i - j):
                ataques += 1
    return ataques

# Função de aptidão: maximizar o número de pares não atacantes


def f(solucao):
    return 28 - num_pares_atacando(solucao)

# Função que gera uma perturbação (nova solução candidata) baseada na solução atual


def perturb(solucao):
    nova_solucao = solucao.copy()
    # Escolhe uma coluna aleatória para perturbar
    col = np.random.randint(0, len(solucao))
    # Muda a rainha para uma nova linha aleatória
    nova_solucao[col] = np.random.randint(0, len(solucao))
    return nova_solucao

# Função de resfriamento (diferentes métodos)


def cooling_schedule(T, cooling_rate, method='geometric'):
    if method == 'geometric':
        return T * cooling_rate
    elif method == 'linear':
        return T - cooling_rate
    elif method == 'logarithmic':
        return T / (1 + np.log(1 + cooling_rate))
    else:
        raise ValueError("Método de resfriamento não reconhecido")

# Função principal que implementa a Têmpera Simulada


def tempera_simulada_8_rainhas(it_max=1000, T_init=100, sigma=0.2, cooling_rate=0.99, max_sem_melhora=100, method='geometric'):
    # Iniciar com uma solução aleatória
    solucao_atual = np.random.randint(0, 8, size=8)
    f_atual = f(solucao_atual)

    f_otimos = [f_atual]
    solucao_unica = set()
    solucao_unica.add(tuple(solucao_atual))

    T = T_init
    i = 0
    iter_sem_melhora = 0

    start_time = time.time()

    while i < it_max and len(solucao_unica) < 92 and iter_sem_melhora < max_sem_melhora:
        solucao_cand = perturb(solucao_atual)
        f_cand = f(solucao_cand)

        delta_f = f_cand - f_atual
        p_ij = np.exp(-delta_f / T) if delta_f < 0 else 1

        if f_cand > f_atual or p_ij >= np.random.uniform(0, 1):
            solucao_atual = solucao_cand
            f_atual = f_cand
            iter_sem_melhora = 0
            solucao_unica.add(tuple(solucao_atual))
        else:
            iter_sem_melhora += 1

        f_otimos.append(f_atual)
        T = cooling_schedule(T, cooling_rate, method)
        i += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Tempo de execução:", elapsed_time)

    return f_otimos, solucao_unica

# Função para plotar o progresso do valor ótimo


def plot_optimization_progress(f_otimos):
    plt.plot(f_otimos)
    plt.xlabel('Iterações')
    plt.ylabel('Número de pares não atacantes')
    plt.title('Progresso da Otimização (Têmpera Simulada)')
    plt.show()

# Função para visualizar a superfície da função (opcional)


def plot_function_surface():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x_axis = np.linspace(-1, 2, 1000)
    X, Y = np.meshgrid(x_axis, x_axis)

    def f(x, y):
        return x**2 * np.sin(4 * np.pi * x) - y * np.sin(4 * np.pi * y + np.pi) + 1

    ax.plot_surface(X, Y, f(X, Y), cmap='viridis')
    plt.show()


# ---- Execução do Algoritmo ---- #
plot_function_surface()  # Opcional

f_otimos, solucao_final = tempera_simulada_8_rainhas(
    it_max=10000, T_init=100, sigma=0.2, cooling_rate=0.99, max_sem_melhora=100, method='geometric')

# Plotar o progresso da otimização
plot_optimization_progress(f_otimos)

# Mostrar a solução final encontrada
print("Número de soluções distintas encontradas:", len(solucao_final))
print("Melhor solução encontrada:", max(solucao_final, key=lambda s: f(s)))
print("Número de pares não atacantes na melhor solução:",
      f(max(solucao_final, key=lambda s: f(s))))
