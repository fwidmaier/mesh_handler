import math

from mesh import *


class Plane(Mesh):
    """
    Implements a class for generating planes.
    """
    def __init__(self, width=1, height=1):
        """
        :param width: (float) The width of the plane
        :param height: (float) The height of the plane
        """
        super().__init__()
        self.name = "Plane"
        for i in range(2):
            self.vertices += [Vertex(pow(-1, i) * width/2, pow(-1, j) * height/2, 0) for j in range(2)]

        # a plane consists just really of one face
        self.faces.append(Face(self.vertices[2], self.vertices[3], self.vertices[1], self.vertices[0]))


class Cube(Mesh):
    """
    Implements a class for generating cubes.
    """
    def __init__(self, a=1):
        """
        :param a: (float) The length of the edges
        """
        super().__init__()
        self.name = "Cube"

        for i in range(2):
            self.vertices += [Vertex(pow(-1, i) * a, pow(-1, j) * a, 1) for j in range(2)]
            self.vertices += [Vertex(pow(-1, i) * a, pow(-1, j) * a, -1) for j in range(2)]

        # not really the most aesthetic way of doing this - but it works fine
        self.faces.append(Face(self.vertices[0], self.vertices[1], self.vertices[3], self.vertices[2]))
        self.faces.append(Face(self.vertices[6], self.vertices[7], self.vertices[5], self.vertices[4]))
        self.faces.append(Face(self.vertices[1], self.vertices[5], self.vertices[7], self.vertices[3]))
        self.faces.append(Face(self.vertices[2], self.vertices[6], self.vertices[4], self.vertices[0]))
        self.faces.append(Face(self.vertices[0], self.vertices[4], self.vertices[5], self.vertices[1]))
        self.faces.append(Face(self.vertices[3], self.vertices[7], self.vertices[6], self.vertices[2]))


class Cone(Mesh):
    """
    Implements a class for generating Cones.
    """
    def __init__(self, radius=1, height=1, n=20):
        """
        :param radius: (float) The radius of the base disc
        :param height: (float) The height of the cone
        :param n: (int) The number of vertices to form the bottom disc
        """
        super().__init__()
        self.name = "Cone"

        self.vertices.append(Vertex(0, 0, 0))
        self.vertices.append(Vertex(0, 0, height))
        for i in range(n):
            self.vertices.append(Vertex(radius * math.cos(2 * math.pi * (i/n)),
                                        radius * math.sin(2 * math.pi * (i/n)), 0))

        for i in range(n-1):
            self.faces.append(Face(self.vertices[i + 2], self.vertices[i + 3], self.vertices[1]))
            self.faces.append(Face(self.vertices[i + 3], self.vertices[i + 2], self.vertices[0]))
        # closing off the remaining faces
        self.faces.append(Face(self.vertices[-1], self.vertices[2], self.vertices[1]))
        self.faces.append(Face(self.vertices[2], self.vertices[-1], self.vertices[0]))


class Cylinder(Mesh):
    """
    Implements a class for generating (closed) Cylinders.
    """
    def __init__(self, radius=1, height=1, n=20):
        """
        :param radius: (float) The radius of the cylinder
        :param height: (float) The height of the cylinder
        :param n: (int) The number of vertices to form the top/bottom disc
        """
        super().__init__()
        self.name = "Cylinder"

        self.vertices.append(Vertex(0, 0, 0))
        self.vertices.append(Vertex(0, 0, height))
        for i in range(n):
            self.vertices.append(Vertex(radius * math.cos(2 * math.pi * (i / n)),
                                        radius * math.sin(2 * math.pi * (i / n)), 0))
        for i in range(n):
            self.vertices.append(Vertex(radius * math.cos(2 * math.pi * (i / n)),
                                        radius * math.sin(2 * math.pi * (i / n)), height))

        for i in range(n):
            self.faces.append(Face(self.vertices[i + 2], self.vertices[i + 3], self.vertices[i + n + 2]))
            self.faces.append(Face(self.vertices[i + 2], self.vertices[i + n + 2], self.vertices[i + n + 1]))
        for i in range(1, n-1):
            self.faces.append(Face(self.vertices[0], self.vertices[i + 3], self.vertices[(i+2)]))
            self.faces.append(Face(self.vertices[i+n+1], self.vertices[i + n + 2], self.vertices[1]))
        # closing off the remaining faces
        self.faces.append(Face(self.vertices[0], self.vertices[2], self.vertices[n + 1]))
        self.faces.append(Face(self.vertices[3], self.vertices[2], self.vertices[0]))
        self.faces.append(Face(self.vertices[2 * n], self.vertices[2 * n + 1], self.vertices[1]))
        self.faces.append(Face(self.vertices[1], self.vertices[-1], self.vertices[n+2]))
