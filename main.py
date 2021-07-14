from mesh.objects.parameterized import *
from mesh.objects import *

# writing out all possible objects:
OBJFile.write("out/plane.obj", Plane())
OBJFile.write("out/cube.obj", Cube())
OBJFile.write("out/cone.obj", Cone())
OBJFile.write("out/cylinder.obj", Cylinder())

# Of course, one may crank up the resolution by increasing n for the parameterised meshes
# In this example, we take the standard values just for simplicity
OBJFile.write("out/torus.obj", Torus())
OBJFile.write("out/trefoil.obj", TrefoilKnot())
OBJFile.write("out/klein-bottle.obj", KleinBottle())
OBJFile.write("out/moebius.obj", MoebiusStrip())
OBJFile.write("out/apple.obj", Apple())
