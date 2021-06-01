'''A simple example of how to use the Blueprint module (v0.1)'''

# global imports
from blueprint import Blueprint, HOUSE

# make a Blueprint
b = Blueprint(30, 30)

# Try and inspect a point!
print(b.inspect(1, 1, 0))

# Look at the documentation
print(help(Blueprint))

# Plot a house onto the Blueprint
b.plot(HOUSE)
# Try and inspect a point again!
print(b.inspect(1, 1, 0))

# Print the Blueprint to the console
b.print()

# Create a temporary image of the Blueprint
b.show()
# Save an image of the blueprint to 'floorplan.png'
b.save('floorplan')
# Clear the blueprint of all annotations
b.clear()
# Print the empty blueprint
b.print()

# Enable optimizations and reprint the blueprint to see the differences
b.enableOptimizations()
b.plot(HOUSE)
b.print()