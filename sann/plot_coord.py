import pandas as pd
import matplotlib.pyplot as plt

# Função para ler um arquivo CSV e retornar um DataFrame com as coordenadas
def ler_arquivo_csv(nome_arquivo):
    df = pd.read_csv(nome_arquivo)
    return df

# Função para plotar as coordenadas de um DataFrame
def plotar_coordenadas(df, cor, label):
    plt.scatter(df['Componente1'], df['Componente2'], c=cor, label=label)

# Nomes dos arquivos CSV
arquivo1 = 'output/5/dados_out.csv'
arquivo2 = 'output/5/dados_in.csv'
arquivo3 = 'output/5/dados_ext.csv'

# Leitura dos arquivos CSV
dados1 = ler_arquivo_csv(arquivo1)
dados2 = ler_arquivo_csv(arquivo2)
dados3 = ler_arquivo_csv(arquivo3)

# Plotagem das coordenadas
plotar_coordenadas(dados1, 'r', 'Arquivo 1')
plotar_coordenadas(dados2, 'g', 'Arquivo 2')
plotar_coordenadas(dados3, 'b', 'Arquivo 3')

# Configurações do gráfico
plt.title('Coordenadas Sobrepostas')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

# Exibição do gráfico
plt.show()

print(dados1)
print(dados2)
print(dados3)
