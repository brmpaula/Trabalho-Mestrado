import cv2
import pandas as pd
import numpy as np

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

# Ler os dois arquivos CSV (suponha que eles contenham coordenadas x e y de vértices)
shape1_data = read_csv_shape('tst/out.csv')  # Ex: [(x1, y1), (x2, y2), ...] - Forma externa
shape2_data = read_csv_shape('tst/in.csv')  # Outra forma inscrita, se houver - Forma interna

# Criar uma imagem em branco
image_size = (500, 500)  # (altura, largura, canais de cor)
image = np.zeros(image_size, dtype=np.uint8)

# Calcular o fator de escala com base na forma externa (shape1)
scale_factor = calculate_scale_factor(shape1_data, image_size)

# Escalar ambas as formas usando o mesmo fator de escala
pts_shape1 = scale_points_proportionally(shape1_data, scale_factor)
pts_shape1 = centralize_shape(pts_shape1, image_size).reshape((-1, 1, 2))

pts_shape2 = scale_points_proportionally(shape2_data, scale_factor)
pts_shape2 = centralize_shape(pts_shape2, image_size).reshape((-1, 1, 2))

# Desenhar a primeira forma abstrata (preenchida) a partir dos pontos
cv2.fillPoly(image, [pts_shape1], 255)  # Cor verde para a primeira forma

# Desenhar a segunda forma (inscrita) a partir dos pontos
cv2.polylines(image, [pts_shape2], isClosed=True, color=100, thickness=2)  # Cor azul para a segunda forma



# Salvar a imagem
cv2.imwrite('output_abstract_shapes_scaled_centered_proportional.png', image)

