import numpy as np
import matplotlib.pyplot as plt

# Função que gera uma perturbação (nova solução candidata) baseada na solução atual
def perturbacao(x, xl, xu, sigma):
    """
    Perturba a solução atual 'x' gerando uma nova solução candidata
    Adiciona um ruído gaussiano e garante que os novos valores estejam dentro dos limites definidos.
    
    Parâmetros:
    - x: vetor com a solução atual
    - xl: limites inferiores das variáveis
    - xu: limites superiores das variáveis
    - sigma: desvio padrão da perturbação (define a intensidade da perturbação)
    
    Retorna:
    - x_cand: nova solução candidata
    """
    # Adiciona perturbação gaussiana (normal) à solução atual
    x_cand = x + np.random.normal(loc=0, scale=sigma, size=x.shape)
    
    # Garante que a solução candidata não ultrapasse os limites definidos (xl, xu)
    for i in range(x_cand.shape[0]):
        if x_cand[i] < xl[i]:
            x_cand[i] = xl[i]
        if x_cand[i] > xu[i]:
            x_cand[i] = xu[i]
    
    return x_cand

# Função a ser minimizada (bidimensional)
def f(x, y):
    """
    Função de teste para otimização, f(x, y) é uma combinação de senos e quadrados.
    
    Parâmetros:
    - x: primeira variável
    - y: segunda variável
    
    Retorna:
    - O valor da função f(x, y)
    """
    return x**2 * np.sin(4 * np.pi * x) - y * np.sin(4 * np.pi * y + np.pi) + 1

# Visualização da superfície da função (opcional)
def plot_function_surface():
    """
    Gera uma visualização 3D da superfície da função f(x, y) no intervalo [-1, 2].
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    x_axis = np.linspace(-1, 2, 1000)  # Gera os valores de x e y no intervalo
    X, Y = np.meshgrid(x_axis, x_axis) # Cria uma grade de valores
    
    ax.plot_surface(X, Y, f(X, Y), cmap='viridis')  # Plota a superfície 3D
    plt.show()

# Função principal que implementa a Têmpera Simulada
def simulated_annealing(it_max=1000, T_init=100, sigma=0.2, xl=(-1, -1), xu=(2, 2), cooling_rate=0.99):
    """
    Implementa o algoritmo de Têmpera Simulada para minimizar a função f(x, y).
    
    Parâmetros:
    - it_max: número máximo de iterações
    - T_init: temperatura inicial
    - sigma: desvio padrão da perturbação
    - xl: limites inferiores para as variáveis
    - xu: limites superiores para as variáveis
    - cooling_rate: taxa de resfriamento da temperatura
    
    Retorna:
    - f_otimos: lista com os valores da função em cada iteração (progresso do algoritmo)
    """
    # Iniciar com uma solução aleatória dentro dos limites definidos
    x_opt = np.random.uniform(low=xl, high=xu)
    f_opt = f(x_opt[0], x_opt[1])  # Avaliar a função na solução inicial
    
    # Armazenar o histórico de soluções ótimas
    f_otimos = [f_opt]
    
    T = T_init  # Definir a temperatura inicial
    i = 0  # Contador de iterações
    
    # Início do loop da Têmpera Simulada
    while i < it_max:
        # Gera uma nova solução candidata com uma perturbação
        x_cand = perturbacao(x_opt, xl, xu, sigma)
        f_cand = f(x_cand[0], x_cand[1])  # Avaliar a função na solução candidata
        
        # Probabilidade de aceitar uma solução pior
        delta_f = f_cand - f_opt
        p_ij = np.exp(-delta_f / T) if delta_f > 0 else 1
        
        # Verifica se a nova solução deve ser aceita
        if f_cand < f_opt or p_ij >= np.random.uniform(0, 1):
            x_opt = x_cand
            f_opt = f_cand
        
        # Armazenar o valor ótimo atual
        f_otimos.append(f_opt)
        
        # Atualizar a temperatura (resfriamento)
        T *= cooling_rate
        
        # Incrementa o contador de iterações
        i += 1
    
    return f_otimos

# Função para plotar o progresso do valor ótimo
def plot_optimization_progress(f_otimos):
    """
    Plota o progresso da função objetivo durante o processo de otimização.
    
    Parâmetros:
    - f_otimos: lista de valores da função ao longo das iterações
    """
    plt.plot(f_otimos)
    plt.xlabel('Iterações')
    plt.ylabel('Valor da função f(x, y)')
    plt.title('Progresso da Minimização (Têmpera Simulada)')
    plt.show()


# ---- Execução do Algoritmo ---- #

# (Opcional) Plotar a superfície da função a ser minimizada
plot_function_surface()

# Executar a Têmpera Simulada
f_otimos = simulated_annealing()

# Plotar o progresso da otimização
plot_optimization_progress(f_otimos)