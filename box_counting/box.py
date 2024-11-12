import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from PIL import Image

# Função para contar o número de quadrados (ou subintervalos) com pontos
def box_counting(fractal_points, epsilon):
    # Definir limites da caixa para cobrir a fractal
    x_min, x_max = min(fractal_points[:, 0]), max(fractal_points[:, 0])
    y_min, y_max = min(fractal_points[:, 1]), max(fractal_points[:, 1])

    # Número de subintervalos ao longo de cada eixo
    num_boxes_x = int((x_max - x_min) / epsilon) + 1  # +1 para incluir a borda
    num_boxes_y = int((y_max - y_min) / epsilon) + 1  # +1 para incluir a borda

    # Inicializar uma matriz de zeros para as caixas
    boxes = np.zeros((num_boxes_x, num_boxes_y))

    #Preencher as caixas com pontos (PRECISA MUDAR)
    for point in fractal_points:
        x_idx = min(int((point[0] - x_min) / epsilon), num_boxes_x - 1)
        y_idx = min(int((point[1] - y_min) / epsilon), num_boxes_y - 1)
        boxes[x_idx, y_idx] = 1  # Marcar caixa com um ponto

    # Contar o número de caixas não vazias
    return boxes 

# Função para calcular a dimensão fractal
def fractal_dimension(fractal_points, epsilons):
    counts = []
    frames = []
    for epsilon in epsilons:
        boxes = box_counting(fractal_points, epsilon)
        N = np.sum(boxes > 0)
        counts.append(N)
        array = boxes        

        # Configurando o plot para cada frame
        fig, ax = plt.subplots()
        ax.imshow(array, cmap='gray')  # 'gray' pinta o 1 como preto e o 0 como branco
        ax.axis('off')  # Desativa eixos para um visual mais limpo
        
        ax.text(0.5, 0.5, f'Epsilon: {epsilon}', color='white', fontsize=12, ha='center', va='center',
            transform=ax.transAxes, bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.3'))


        # Salva o frame atual como imagem
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frames.append(Image.fromarray(image))
        plt.close(fig)
        
    
    frames[0].save(
        'grid_animation.gif', 
        save_all=True, 
        append_images=frames[1:], 
        duration=200,  # Tempo de exibição de cada frame em ms
        loop=0         # Loop infinito
    )
    
    # Ajustar a linha pelo método dos mínimos quadrados
    log_epsilons = np.log(1 / np.array(epsilons))
    log_counts = np.log(counts)
    
    coeffs = np.polyfit(log_epsilons, log_counts, 1)
    D = coeffs[0]

    # Plotando a curva log-log  
    plt.plot(log_epsilons, log_counts, 'bo', label='Dados')
    plt.plot(log_epsilons, np.polyval(coeffs, log_epsilons), 'r-', label=f'Ajuste Linear: D = {D:.4f}')
    plt.xlabel('log(1/epsilon)')
    plt.ylabel('log(N(epsilon))')
    plt.legend()
    plt.show()
    
    
    
    array_para_csv(log_epsilons, log_counts)
    
    

    return D


def array_para_csv(array1,array2):
    # Nome do arquivo CSV
    nome_arquivo = 'coordenadas.csv'

    # Verifique se os arrays têm o mesmo tamanho
    if len(array1) == len(array2):
        # Abre o arquivo para escrita
        with open(nome_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
        
        # Escreve o cabeçalho (opcional)
            writer.writerow(['Coordenada1', 'Coordenada2'])
        
        # Escreve cada par de coordenadas
            for coord1, coord2 in zip(array1, array2):
                writer.writerow([coord1, coord2])

        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    else:
        print("Os arrays têm tamanhos diferentes e não podem ser combinados.")


   
def csv_para_array(caminho_arquivo):
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        array = [linha for linha in leitor_csv]
    return array
    
    
def read_csv_shape(filename):
    df = pd.read_csv(filename)
    return df.values




# Exemplo de uso com um conjunto de pontos de um fractal

if __name__ == "__main__":
    # Gerar alguns pontos fractais de exemplo (pontos aleatórios dentro de um quadrado)
    shape1_data = read_csv_shape('1/out.csv')  # Ex: [(x1, y1), (x2, y2), ...] - Forma externa
    shape2_data = read_csv_shape('1/in.csv')  # Outra forma inscrita, se houver - Forma interna
    
        
   
    fractal_points = shape1_data

    # Definir valores de epsilon para calcular a dimensão fractal
    epsilons = np.logspace(-2.0,0, 500)

    # Calcular e exibir a dimensão fractal
    D = fractal_dimension(fractal_points, epsilons)
    print(f"Dimensão fractal calculada: {D:.4f}")



