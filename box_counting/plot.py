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
nome_arquivo = 'coordenadas.csv'

# Array para armazenar os valores da coordenada escolhida
array_coordenada1 = []
array_coordenada2 = []
D = []
num = []


# Abra o arquivo CSV para leitura
with open(nome_arquivo, mode='r') as file:
    reader = csv.reader(file)
    
    # Pule o cabeçalho
    next(reader)
    
    # Para cada linha, extraia a coordenada desejada e adicione ao array
    for linha in reader:
        valor0 = linha[0]
        valor1 = linha[1]
        
        array_coordenada1.append(float(valor0))  # Converte para float ou int, se necessário
        array_coordenada2.append(float(valor1))  # Converte para float ou int, se necessário
        
        if len(array_coordenada1) > 1 and len(array_coordenada2) > 1:
            coeffs = np.polyfit(array_coordenada1, array_coordenada2, 1)
            D.append(coeffs[0])
            num.append(float(valor1))
          

average_thickness = np.mean(D)

plt.figure()
plt.hist(D, bins=50, color='blue', alpha=0.7)
plt.title('Distribuição das Dimenções Fractais')
plt.xlabel('Dimenções')
plt.ylabel('Frequência')
# Adicionar uma linha vertical no valor da média
plt.axvline(average_thickness, color='red', linestyle='dashed', linewidth=2, label=f'Média: {average_thickness:.2f}')

# Adicionar o valor da média no gráfico
plt.text(average_thickness, plt.gca().get_ylim()[1] * 0.9, f'{average_thickness:.2f}', color='red', ha='center', va='top')
             

# Adicionar legenda
plt.legend()

plt.show()


plt.plot(num, D, 'bo', label='Dados')
plt.xlabel('Max Numero de Caixa')
plt.ylabel('Dimencao Fractal')
plt.legend()
plt.show()
