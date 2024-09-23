from utils.gen import AlgoGenCont
import matplotlib.pyplot as plt
import pandas as pd


# Configuração inicial para rodar o algoritmo
pop_size = 10
dim = 20
gen = 10
tax_recomb = 0.85
num_runs = 100

# Inicializar listas para armazenar resultados
results_can = []
results_float = []

# Executar os algoritmos genéticos para 100 rodadas
for _ in range(num_runs):
    algo_can = AlgoGenCont(
        N=pop_size, p=dim, nd=1, lim_inf=-10, lim_sup=10,
        recomb=tax_recomb, is_can=True, qtd_geracoes=gen)

    algo_float = AlgoGenCont(
        N=pop_size, p=dim, nd=1, lim_inf=-10, lim_sup=10,
        recomb=tax_recomb, is_can=False, tam_torneio=5, qtd_geracoes=gen)

    # Executar e coletar resultados de cada geração
    results_can.append(algo_can.execute())
    results_float.append(algo_float.execute())

# Criar DataFrames para as gerações canônicas e não canônicas
colunas = ['Geração', 'Menor Aptidão',
           'Maior Aptidão', 'Aptidão Média', 'Desvio Padrão']

# Resultados Canônicos
can_df = pd.DataFrame(
    [item for sublist in results_can for item in sublist], columns=colunas)

# Resultados Não Canônicos
float_df = pd.DataFrame(
    [item for sublist in results_float for item in sublist], columns=colunas)

# Exibir as tabelas e gráficos
print("Tabela de Gerações Canônicas")
print(can_df)
can_df['Desvio Padrão'].plot(title="Desvio Padrão - Gerações Canônicas")
plt.xlabel("Geração")
plt.ylabel("Desvio Padrão")
plt.show()

print("\nTabela de Gerações Não Canônicas")
print(float_df)
float_df['Desvio Padrão'].plot(title="Desvio Padrão - Gerações Não Canônicas")
plt.xlabel("Geração")
plt.ylabel("Desvio Padrão")
plt.show()
