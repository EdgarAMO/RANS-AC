from fluidfoam import readmesh
from fluidfoam import readvector
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

sol = '/home/edgar/OpenFOAM/edgar-7/run/actuatorCylinderA'

# coordinates
x, y, z = readmesh(sol, False)

# velocity field
vel = readvector(sol, '495', 'U', False)

# flip them around
X = x.reshape(258, 338)
Y = y.reshape(258, 338)
Y = Y[::-1, :]

# magnitude of the velocity field
magU = np.sqrt( vel[0, :]**2 + vel[1, :]**2 )
magU.resize(258, 338)
magU = magU[::-1, :]

# circle represents the turbine
circle1 = Circle((15,    0.000), 5.0, color='blue', fill=False)
circle2 = Circle((-7.5,  12.99), 5.0, color='blue', fill=False)
circle3 = Circle((-7.5, -12.99), 5.0, color='red',  fill=False)

# plot the contours
fig = plt.figure(figsize=(7.86, 6))
plt.rc('font', size=18)
plt.rcParams["font.family"] = "monospace"
plt.title('VAWT wake @ TSR=3.0')
plt.xlabel('x')
plt.ylabel('y')
ax = fig.add_subplot(1,1,1)
img = ax.imshow(magU,
                interpolation='bilinear',
                cmap='jet',
                extent=[X.min(), X.max(), Y.min(), Y.max()])

##cbar = fig.colorbar(ax=ax,
##                    mappable=img,
##                    orientation='horizontal',
##                    pad=0.3,
##                    label='m/s')

ax.text(24,   0.000, '{0:.3f}'.format(0.389), weight='bold', color='white',fontsize=12)
ax.text(-24,  12.99, '{0:.3f}'.format(0.407), weight='bold', color='white',fontsize=12)
ax.text(-24, -12.99, '{0:.3f}'.format(0.380), weight='bold', color='white',fontsize=12)

ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(circle3)

plt.show()


