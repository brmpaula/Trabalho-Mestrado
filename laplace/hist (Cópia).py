# Plotar o histograma das distâncias

import matplotlib.pyplot as plt
import csv
import numpy as np

# Função para ler um arquivo CSV e convertê-lo em um array
def csv_para_array(caminho_arquivo):
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        array = [linha for linha in leitor_csv]
    return array

# Exemplo de uso
nome_arquivo = 'dist.csv'

# Array para armazenar os valores da coordenada escolhida
array_coordenada1 = []
array_coordenada2 = []


# Abra o arquivo CSV para leitura
with open(nome_arquivo, mode='r') as file:
    reader = csv.reader(file)
    
    # Pule o cabeçalho
    next(reader)
    
    # Para cada linha, extraia a coordenada desejada e adicione ao array
    for linha in reader:
        valor1 = linha[0]
        valor2 = linha[1]
        
        array_coordenada1.append(float(valor0))  # Converte para float ou int, se necessário
        array_coordenada2.append(float(valor1))  # Converte para float ou int, se necessário
        log_epsilons = np.log(1 / np.array(array_coordenada1))
        log_counts = np.log(array_coordenada2)



print("Array da coordenada desejada:", array_coordenada)

log_epsilons = np.log(1 / np.array(epsilons))
log_counts = np.log(counts)
    
coeffs = np.polyfit(log_epsilons, log_counts, 1)
D = coeffs[0]


average_thickness = np.mean(distances)

thickness = 0

plt.figure()
plt.hist(distances, bins=1000, color='blue', alpha=0.7)
plt.title('Distribuição das Distâncias entre Equipotenciais dos Extremos')
plt.xlabel('Distância (pixels)')
plt.ylabel('Frequência')
# Adicionar uma linha vertical no valor da média
plt.axvline(average_thickness, color='red', linestyle='dashed', linewidth=2, label=f'Média Laplace: {average_thickness:.2f}')

# Adicionar o valor da média no gráfico
plt.text(average_thickness, plt.gca().get_ylim()[1] * 0.9, f'{average_thickness:.2f}', color='red', ha='center', va='top')
             
# Adicionar uma linha vertical no valor da média
plt.axvline(thickness, color='green', linestyle='dashed', linewidth=2, label=f'Média Base: {thickness:.2f}')

# Adicionar o valor da média no gráfico
plt.text(thickness, plt.gca().get_ylim()[1] * 0.9, f'{thickness:.2f}', color='green', ha='center', va='top')

# Adicionar legenda
plt.legend()

plt.show()
