import pygame

# Create a Vector2 object
my_vector = pygame.math.Vector2(-1, 0)

# Get the polar coordinates (radius, angle)
polar_coords = my_vector.as_polar()

# The angle is the second element in the tuple
angle_in_degrees = polar_coords[1]

print(f"The angle of the vector is: {angle_in_degrees} degrees")