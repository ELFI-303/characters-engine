from object import Camera,Sphere,GetCenter,NormVect
from math import sqrt,atan
import matplotlib.pyplot as plt
import matplotlib.patches as patches

monde = []
camera = Camera()
camera.angle = (0,0)
plan = camera.GetPlan()
sphere = Sphere()
sphere.position = (80,0,0)
monde.append(sphere.GetMat(7000))



array = camera.ElementInView(monde[0])


fig, ax = plt.subplots()

# Loop through each triangle and plot it
for triangle in array:
    # Create a Polygon patch from the triangle vertices
    polygon = patches.Polygon(triangle, closed=True, edgecolor='black', facecolor='skyblue', alpha=0.5)
    ax.add_patch(polygon)

# Set plot limits and aspect ratio
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')

# Display the plot
plt.show()
"""
tr,tl,br,bl = getCam(camera)
square_width = sqrt((tr[0]-tl[0])**2+(tr[1]-tl[1])**2+(tr[2]-tl[2])**2)
square_height = sqrt((tr[0]-br[0])**2+(tr[1]-br[1])**2+(tr[2]-br[2])**2)

near_plan = tr,tl,br,bl

far_plan = getPlan(near_plan,100)

print(near_plan,far_plan)
"""