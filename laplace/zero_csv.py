import csv

# Contar quantos zeros existem no arquivo CSV
def contar_zeros(caminho_csv):
    contador_zeros = 0
    
    # Abrir o arquivo CSV
    with open(caminho_csv, 'r') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        
        # Percorrer cada linha do arquivo CSV
        for linha in leitor:
            # Verificar cada célula da linha
            for celula in linha:
                if celula == '0':  # Verifica se a célula é um zero
                    contador_zeros += 1
                    
    return contador_zeros
    
 
 # Função para encontrar o valor mínimo em um arquivo CSV
def encontrar_valor_minimo(caminho_csv):
    valor_minimo = None
    
    # Abrir o arquivo CSV
    with open(caminho_csv, 'r') as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        
        # Percorrer cada linha do arquivo CSV
        for linha in leitor:
            # Verificar cada célula da linha
            for celula in linha:
                try:
                    # Converter o valor da célula para float
                    valor = float(celula)
                    
                    # Atualizar o valor mínimo, se necessário
                    if valor_minimo is None or valor < valor_minimo:
                        valor_minimo = valor
                except ValueError:
                    # Ignorar valores não numéricos
                    pass
                    
    return valor_minimo


caminho_arquivo = 'dist.csv'  # Substitua pelo caminho do seu arquivo CSV
quantidade_zeros = contar_zeros(caminho_arquivo)
print(f"A quantidade de zeros no arquivo é: {quantidade_zeros}")

valor_minimo = encontrar_valor_minimo(caminho_arquivo)
print(f"O valor mínimo no arquivo é: {valor_minimo}")

