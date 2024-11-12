# Adapteed from https://levelup.gitconnected.com/solving-2d-heat-equation-numerically-using-python-3334004aa01a
# and by the Laplacian solver by C. Rummel and Victor Mello, January 2025 (BTTF !)
# by Bruno Mota, metaBIO, 2024

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import cv2
import random
import pandas as pd

print("2D PacMan melter")

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



L = 192 # Box size
max_iter_time = 128 # Total time steps

# PDE solver parameters
alpha = 2
delta_x = 1
delta_t = (delta_x ** 2) / (4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j)
u = np.empty((max_iter_time, L, L))

# Ler os dois arquivos CSV (suponha que eles contenham coordenadas x e y de vértices)
shape1_data = read_csv_shape('out.csv')  # Ex: [(x1, y1), (x2, y2), ...] - Forma externa
shape2_data = read_csv_shape('in.csv')  # Outra forma inscrita, se houver - Forma interna

# Criar uma imagem em branco
image_size = (L, L)  # (altura, largura, canais de cor)
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

	
# Set the boundary conditions
high_pot = 100.0
low_pot = 0.0

# Initial condition everywhere else inside the grid
u_initial = 10

# Set initial conditions
u.fill(u_initial)

# Function to apply boundary conditions
def apply_boundary_conditions(u_k):
    u_k[image == 100] = high_pot  # Inside inner ellipse
    u_k[image == 0] = low_pot     # Outside outer ellipse
    return u_k

# Apply initial boundary conditions
u[0] = apply_boundary_conditions(u[0])

# Create a mask for the boundary conditions
mask = (image != 100) & (image != 0)

# Iterates the heat map over time using vector magic 
def calculate(u):
    for k in range(0, max_iter_time - 1):
        u_k = u[k]
        u_k1 = apply_boundary_conditions(u[k + 1]) 
               
        # Calculate the new values using vector magic 
        update_values = np.zeros_like(u_k1)
        update_values[1:-1, 1:-1][mask[1:-1, 1:-1]] = gamma * (
            u_k[2:, 1:-1][mask[1:-1, 1:-1]] + 
            u_k[:-2, 1:-1][mask[1:-1, 1:-1]] + 
            u_k[1:-1, 2:][mask[1:-1, 1:-1]] + 
            u_k[1:-1, :-2][mask[1:-1, 1:-1]] - 
            4 * u_k[1:-1, 1:-1][mask[1:-1, 1:-1]]
        ) + u_k[1:-1, 1:-1][mask[1:-1, 1:-1]]
        
        # Update u_k1 with the calculated values only for points outside the boundary conditions
        u_k1[1:-1, 1:-1][mask[1:-1, 1:-1]] = update_values[1:-1, 1:-1][mask[1:-1, 1:-1]]
        u[k + 1] = u_k1
        
        print(u_k.min(), u_k.max())
        
    return u

# Calculate the solution
u = calculate(u)



# Plot the temperature field, some equipotential contours and gradient lines
def plotheatmap(u_k, k):
    plt.clf()
    plt.title(f"Temperature at t = {k * delta_t:.3f} unit time")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.pcolormesh(u_k, cmap='gist_earth', vmin=0, vmax=100)
    plt.colorbar()
    plt.contour(u_k, levels=equipotential_values, colors='black', linestyles='solid', extent=(0, L-1, 0, L-1))

    # Compute the gradient for streamlines
    dy, dx = np.gradient(u_k)
    y, x = np.arange(L), np.arange(L)
    plt.streamplot(x, y, -dx, -dy, color='white', linewidth=0.3)

    return plt

def animate(k):
    plotheatmap(u[k], k)

equipotential_values = [25, 50, 75, 95]

# Export the plot to a file
fig = plt.figure()
anim = animation.FuncAnimation(fig, animate, interval=5, frames=max_iter_time, repeat=False)
anim.save("heat_equation_solution.gif", writer='pillow')

# We are done here
phrases = [
    "Avast! Seize that miscreant!",
    "Valar morghulis",
    "Valar dohaeris",
    "ash nazg durbatulûk ash nazg gimbatul ash nazg thrakatulûk agh burzum-ishi krimpatul",
    "The answer is 42",
    "The calculation is left as an exercise to the reader",
    "Nuke it from orbit, it is the only way to be sure",
    "Fool of a Took!",
    "My parole officer will attest to my good character"
]
random_phrase = random.choice(phrases)
print("\033[94m" + random_phrase + "\033[0m")
