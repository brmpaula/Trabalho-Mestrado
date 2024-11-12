# Solve 2D Laplace equation with Dirichlet boundary conditions
# Using pytorch convolutions for speed up the calculations
#
# code for solving Laplace equation is heavily inspired by
# https://www.youtube.com/watch?v=f4Xnz7BHhpE and 
# https://github.com/lukepolson/youtube_channel/blob/main/Python%20Metaphysics%20Series/vid31.ipynb
#
# C. Rummel and Victor Mello, January 2025 (BTTF !)
# Support Center for Advanced Neuroimaging (SCAN)
# University Institute of Diagnostic and Interventional Neuroradiology
# University of Bern, Inselspital, Bern University Hospital, Bern, Switzerland.
#
# Small changes by Bruno Mota, metaBIO, September 2024
#
# For the Newcastle+Rio+Bern (NewcarRiBe) collaboration
import numpy as np
import cv2
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import random
import pandas as pd
from scipy.spatial import distance
import csv


# Função para ler os pontos da forma abstrata a partir do CSV
def read_csv_shape(filename):
    df = pd.read_csv(filename)
    return df.values

# Função para calcular o centroide (centro geométrico) da forma
def calculate_centroid(points):
    centroid_x = np.mean(points[:, 0])
    centroid_y = np.mean(points[:, 1])
    return np.array([centroid_x, centroid_y])

# Função para escalar os pontos mantendo a proporção
def scale_points_proportionally(points, scale_factor):
    scaled_points = points * scale_factor
    return scaled_points.astype(np.float32)

# Função para centralizar os pontos na imagem
def centralize_shape(points, image_size):
    centroid = calculate_centroid(points)
    image_center = np.array([image_size[1] // 2, image_size[0] // 2])  # Centro da imagem (centro_x, centro_y)
    translation = image_center - centroid
    return (points + translation).astype(np.int32)

# Função para calcular o fator de escala para a forma externa
def calculate_scale_factor(external_shape, image_size):
    max_x, max_y = np.max(external_shape, axis=0)
    min_x, min_y = np.min(external_shape, axis=0)
    
    # Tamanho da forma em termos de largura e altura
    shape_width = max_x - min_x
    shape_height = max_y - min_y
    
    # Calcula o fator de escala para manter a proporção e garantir que a forma caiba na imagem
    scale_factor = min((image_size[1] * 0.9) / shape_width, (image_size[0] * 0.9) / shape_height)
    
    return scale_factor

L = 8192 # Box size

# Ler os dois arquivos CSV (suponha que eles contenham coordenadas x e y de vértices)
shape1_data = read_csv_shape('2/out.csv')  # Ex: [(x1, y1), (x2, y2), ...] - Forma externa
shape2_data = read_csv_shape('2/in.csv')  # Outra forma inscrita, se houver - Forma interna

# Criar uma imagem em branco
image_size = (L, L)  # (altura, largura)
mask_external = np.zeros(image_size, dtype=np.uint8)  # Máscara para forma externa
mask_internal = np.zeros(image_size, dtype=np.uint8)  # Máscara para forma interna


# Calcular o fator de escala com base na forma externa (shape1)
scale_factor = calculate_scale_factor(shape1_data, image_size)

# Escalar ambas as formas usando o mesmo fator de escala
pts_shape1 = scale_points_proportionally(shape1_data, scale_factor)
pts_shape1 = centralize_shape(pts_shape1, image_size).reshape((-1, 1, 2))

pts_shape2 = scale_points_proportionally(shape2_data, scale_factor)
pts_shape2 = centralize_shape(pts_shape2, image_size).reshape((-1, 1, 2))

# Desenhar a primeira forma abstrata (preenchida) a partir dos pontos
cv2.fillPoly(mask_external, [pts_shape1], 255)  # 255 para preenchido

# Desenhar a segunda forma (inscrita) a partir dos pontos
cv2.fillPoly(mask_internal, [pts_shape2], 255)  # 255 para preenchido


# Criar a imagem resultante com as áreas internas e externas
image = np.zeros_like(mask_external)


# Define a área externa como 0 (condição de contorno de baixo potencial)
image[mask_external == 255] = 0

# Área entre a forma externa e interna: define como um valor intermediário
image[(mask_external == 255) & (mask_internal == 0)] = 50

# Define a área interna como 100 (condição de contorno de alto potencial)
image[mask_internal == 255] = 100

#Area da Substancia Cinza
area = np.sum(image == 50)

# Encontrar os contornos da imagem
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Calcular o perímetro do primeiro contorno
# O parâmetro "True" indica que o contorno está fechado
perimeter = cv2.arcLength(contours[0], True)

#Calcular a espessura pelo 1 metodo
thickness = area/perimeter


############################################################

# setting the potential
low_pot = -1
high_pot = 1
init_guess = 0

# set the high potential outside the big ellipses
temp1 = np.where(image == 0, high_pot, image)

# set the low potential inside the small ellipses
temp2 = np.where(temp1 == 100, low_pot, temp1)

# set the initial guess between ellipses (initial guess)
potential = np.where(temp2 == 50, init_guess, temp2)

# transform to torch tensor
# speed up the calculation compared to scipy convolution
tensor = torch.zeros(1, 1, potential.shape[0], potential.shape[1])
tensor[0, 0, :, :] = torch.from_numpy(potential).clone().detach()

# create masks for the tensor
mask_high = np.where(tensor == high_pot)
mask_low = np.where(tensor == low_pot)

# kernel as torch tensor
kernel = torch.zeros(1, 1, 3, 3)
kernel[0, 0, 0, 1] = 1. / 4.
kernel[0, 0, 1, 0] = 1. / 4.
kernel[0, 0, 1, 2] = 1. / 4.
kernel[0, 0, 2, 1] = 1. / 4.        

# solution as torch tensor
solution = torch.zeros(1, 1, potential.shape[0], potential.shape[1])
solution[0, 0, :, :] = torch.from_numpy(potential).clone().detach()

# for running the iterations
max_iter = 1000000
tolerance = 1e-4
for n in range(1, max_iter+1):
    # previous solution
    last_solution = solution.detach().clone()

    # torch convolution
    solution = F.conv2d(last_solution, kernel, padding='same')
    
    # re-instate mask potentials in case they have changed during convolution
    solution[mask_high] = high_pot    
    solution[mask_low] = low_pot
    
    # result as numpy array        
    res = solution[0, 0, :, :].numpy()
    iterations = n

    # users may append to an array and look to the convergence          
    rmsc = np.sqrt(((solution - last_solution) ** 2).mean())
    maxc = np.abs(solution - last_solution).max()
    
    # stopping the iterations
    if tolerance is not None and maxc / (high_pot - low_pot) < tolerance:
         break

# plotting the results
# The gradient of the potential field
# field lines (or the thickness direction)

# Specify equipotential values
equipotential_values = [-1,-0.9, -0.5, 0, 0.5,0.9, 1]

gradients = np.gradient(res)
squared_modulus = 20*sum(np.sum(g**2) for g in gradients)

vgrad = np.gradient(res)/squared_modulus

# Define grid
nx, ny = res.shape[0], res.shape[1]
x1 = range(nx)
y1 = range(ny)

# Create plot
fig, ax = plt.subplots()
ax.streamplot(x1, y1, vgrad[1], vgrad[0], density=1.9)
plt.imshow(res, extent=(0, nx-1, 0, ny-1), origin='lower', alpha=0.5, cmap='gist_earth_r')
plt.colorbar(label='Potential')

# Plot equipotential lines
contours = plt.contour(res, levels=equipotential_values, colors='black', linestyles='solid', extent=(0, nx-1, 0, ny-1))
plt.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')

plt.show()

# Inicializar uma lista para armazenar as distâncias entre equipotenciais

paths0 = contours.collections[0].get_paths()

distances = np.zeros((len(paths0[0].vertices)))


# Para cada par de equipotenciais consecutivas, calcular a distância mínima entre seus pontos
for i in range(len(contours.collections) - 1):
    l = 0
    # Obter os vértices das duas equipotenciais adjacentes, se existirem
    paths1 = contours.collections[i].get_paths()
    paths2 = contours.collections[i + 1].get_paths()
   

    # Verificar se os dois contornos têm caminhos
    if len(paths1) > 0 and len(paths2) > 0:
        # Usar o primeiro caminho de cada equipotencial
        equipotential1 = paths1[0].vertices
        equipotential2 = paths2[0].vertices
        
        print(len(equipotential1))
        print(len(equipotential2))
  
        distances = np.resize(distances, len(equipotential1))        

        # Calcular a distância entre cada ponto de equipotential1 e o ponto mais próximo em equipotential2
        for point in equipotential1:            
            dists = distance.cdist([point], equipotential2, 'euclidean')  # Distância euclidiana
            min_dist = np.min(dists)  # Encontrar a menor distância
            distances[l] += min_dist
            l += 1

# Converter a lista de distâncias em um array, se houver dados
if distances.any:
    distances = np.array(distances)

    # Calcular a espessura média entre as equipotenciais dos extremos
    average_thickness = np.mean(distances)

    # Exibir o resultado
    print(f"Espessura média entre as equipotenciais dos extremos: {average_thickness:.2f} pixels")

    # Plotar o histograma das distâncias
    plt.figure()
    plt.hist(distances, bins=40, color='blue', alpha=0.7)
    plt.title('Distribuição das Distâncias entre Equipotenciais dos Extremos')
    plt.xlabel('Distância (pixels)')
    plt.ylabel('Frequência')
   # Adicionar uma linha vertical no valor da média
    plt.axvline(average_thickness, color='red', linestyle='dashed', linewidth=2, label=f'Média Laplace: {average_thickness:.2f}')

    # Adicionar o valor da média no gráfico
    plt.text(average_thickness, plt.gca().get_ylim()[1] * 0.9, f'{average_thickness:.2f}', 
             color='red', ha='center', va='top')
             
    # Adicionar uma linha vertical no valor da média
    plt.axvline(thickness, color='green', linestyle='dashed', linewidth=2, label=f'Média Base: {thickness:.2f}')

    # Adicionar o valor da média no gráfico
    plt.text(thickness, plt.gca().get_ylim()[1] * 0.9, f'{thickness:.2f}', 
             color='green', ha='center', va='top')

    # Adicionar legenda
    plt.legend()

    plt.show()
    
    with open('dist.csv', 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(distances)  # Escreve uma única linha

else:
    print("Não foi possível encontrar equipotenciais válidas nos extremos.")
