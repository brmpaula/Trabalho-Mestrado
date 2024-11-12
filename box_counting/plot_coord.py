import pandas as pd
import matplotlib.pyplot as plt

# Função para ler um arquivo CSV e retornar um DataFrame com as coordenadas
def ler_arquivo_csv(nome_arquivo):
    df = pd.read_csv(nome_arquivo)
    return df

# Função para plotar as coordenadas de um DataFrame
def plotar_coordenadas(df, cor, label):
    plt.scatter(df['x'], df['y'], c=cor, label=label)

# Nomes dos arquivos CSV
arquivo1 = 'real/out.csv'
arquivo2 = 'real/in.csv'

# Leitura dos arquivos CSV
dados1 = ler_arquivo_csv(arquivo1)
dados2 = ler_arquivo_csv(arquivo2)

# Plotagem das coordenadas
plotar_coordenadas(dados1, 'r', 'Arquivo 1')
plotar_coordenadas(dados2, 'g', 'Arquivo 2')

# Configurações do gráfico
plt.title('Coordenadas Sobrepostas')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

# Exibição do gráfico
plt.show()

print(dados1)
print(dados2)
