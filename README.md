# mesh_handler

Provides some classes and methods for quick mesh generation and writing to .obj files.
Allows mesh generation from a given parametrisation of a surface/manifold.

Since the second version it also allows the rendering of (simple) wireframes.

<img src="doc/teapot.png" alt="drawing" width="250"/> <img src="doc/cow.png" alt="drawing" width="250"/> <img src="doc/torus.png" alt="drawing" width="250"/>

## Wireframe rendering

One may launch the interactive viewer through

```bash
python3 wireframe.py out/torus.obj
```

or by

```python
from mesh.obj import OBJFile
from viewer import Viewer

app = Viewer()
torus = OBJFile.read("out/torus.obj", axis="xyz")
app.scene.addObject(torus)
app.show()
```

### Example code

```python
from mesh.obj import OBJFile
from render.scene import *

scene = Scene(500, 500)  # specifying the width and height of the scene (in px)
apple = OBJFile.read("out/apple.obj", axis="xyz")
scene.addObject(apple)

scene.render()
scene.im.show()
```

The code above will generate the following image:

![](doc/apple.png)

## Mesh generation

Some rendered examples of the generated .obj files (some of them can be found in [out](https://github.com/fwidmaier/mesh_handler/tree/v2/out)):

A Klein bottle - immersed in R^3 (rendered with Blender):
![Klein_](https://user-images.githubusercontent.com/80098282/125983125-9538f737-3db1-483c-8ea5-1a3f3a6eb64b.png)
A Moebius strip:
![moeb](https://user-images.githubusercontent.com/80098282/125702241-6d739ab7-56e2-4c67-9e19-88266c3e9129.jpg)
A catenoid:
![catenoid](https://user-images.githubusercontent.com/80098282/125702393-b42d5fa6-4263-49c6-a5db-7becf67bd257.jpg)
A trefoil knot:
![kleeblatschleife2](https://user-images.githubusercontent.com/80098282/125701964-b2c0f171-08d4-4415-be75-f29c0b15e105.jpg)
An apple:
![apple](https://user-images.githubusercontent.com/80098282/125702158-078df84f-e50b-4f91-a5ed-ebc6c2c414e1.jpg)
