# Adapteed from https://levelup.gitconnected.com/solving-2d-heat-equation-numerically-using-python-3334004aa01a
# and by the Laplacian solver by C. Rummel and Victor Mello, January 2025 (BTTF !)
# by Bruno Mota, metaBIO, 2024

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import cv2
import random

print("2D PacMan melter")


L = 192 # Box size
max_iter_time = 128 # Total time steps

# PDE solver parameters
alpha = 2
delta_x = 1
delta_t = (delta_x ** 2) / (4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)

# Initialize solution: the grid of u(k, i, j)
u = np.empty((max_iter_time, L, L))


# Create the boundary conditions using concentric ellipses
img = np.zeros((L,L)) # empty color image

# Outer ellipse
center_coordinatesO = (L // 2, L // 2 )
axesLengthO = (L // 2 - 6, L // 2 - 4)
angle = 0
startAngle = 0
endAngle = 360
color = 50
thickness = -1  # Fill the ellipse
image1 = cv2.ellipse(img, center_coordinatesO, axesLengthO, angle, startAngle, endAngle, color, thickness)

# Inner ellipse with 3 slices carved out
center_coordinatesI = (L // 2, L // 2)
axesLengthI = (L // 3 - 4, L // 3 + 4 )

angle = 0
color = 100
thickness = -1  # Fill the ellipse

# Define the angles for the slices
slices = 9
slice_angle = 360 // slices
  
# List of gap angles
gap_angles = [10, 22, 7, 6, 8, 8, 11, 9, 10, 8, 7]  
default_gap_angle = 8

# Draw each slice
for i in range(slices):
    startAngle = i * slice_angle
    gap_angle = gap_angles[i] if i < len(gap_angles) else default_gap_angle
    endAngle = startAngle + slice_angle - gap_angle
    image2 = cv2.ellipse(image1, center_coordinatesI, axesLengthI, angle, startAngle, endAngle, color, thickness)



# Set the boundary conditions
high_pot = 100.0
low_pot = 0.0

# Initial condition everywhere else inside the grid
u_initial = 10

# Set initial conditions
u.fill(u_initial)

# Function to apply boundary conditions
def apply_boundary_conditions(u_k):
    u_k[image2 == 100] = high_pot  # Inside inner ellipse
    u_k[image2 == 0] = low_pot     # Outside outer ellipse
    return u_k

# Apply initial boundary conditions
u[0] = apply_boundary_conditions(u[0])

# Create a mask for the boundary conditions
mask = (image2 != 100) & (image2 != 0)

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
anim.save("heat_equation_solution_v3.gif", writer='pillow')

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
