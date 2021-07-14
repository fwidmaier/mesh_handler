from mesh import *
import math


def lattice(xrange, yrange, n):
    """
    Generates a lattice for the given parameters.
    In the end it is just a cartesian product of the intervals xrange and yrange
    with n steps in each interval
    :param xrange: (tuple, float)
    :param yrange: (tuple, float)
    :param n: (int) number of steps
    :return: (2-dim list)
    """
    xlen = xrange[1] - yrange[0]
    ylen = yrange[1] - yrange[0]
    xx = [xrange[0] + (xlen/(n - 1)) * i for i in range(n)]
    yy = [yrange[0] + (ylen/(n - 1)) * i for i in range(n)]
    return [[(x, y) for y in yy] for x in xx]


# For further parametrisations: https://mathematikalpha.de/wp-content/uploads/2017/01/19-Raumkurven.pdf


class FromParametrisation(Mesh):
    """
    A class to easily generate meshes for parametrised surfaces/manifolds in R^3
    """
    def __init__(self, parametrisation, xrange=(0, 1), yrange=(0, 1), n=30, quad=False):
        """
        :param parametrisation: (callable) The parametrisation, R^2 -> R^3.
        The parametrisation should map the cartesian product of the intervals xrange
        and yrange to a subset of R^3. It should also be continuous and smooth.
        :param xrange: (tuple, float)
        :param yrange: (tuple, float)
        :param n: (int) number of steps in each interval (for generating the lattice)
        :param quad: (bool) whether or not to use quadrilaterals or triangles in the mesh
        """
        super().__init__()
        self.parametrisation = parametrisation
        self.compileModel(xrange, yrange, n, quad)

    def _mapVerts(self, grid):
        """
        Maps points in a given lattice with the parametrisation.
        :param grid: (list) the lattice
        :return: (list, Vertex) a lattice/grid of mapped vertices
        """
        f = lambda t: Vertex(*self.parametrisation(*t))
        return [list(map(f, v)) for v in grid]

    def _mapFaces(self, verts, quad=False):
        """
        Generates corresponding faces to the mapped vertices
        :param verts: (list, Vertex) the mapped vertices from _mapVerts
        :param quad: (bool) whether or not to use quadrilaterals or triangles in the mesh
        """
        for i in range(len(verts) - 1):
            for j in range(len(verts[0]) - 1):
                if quad:
                    self.faces.append(Face(verts[i][j], verts[i + 1][j], verts[i + 1][j + 1], verts[i][j + 1]))
                else:
                    self.faces.append(Face(verts[i][j], verts[i + 1][j], verts[i + 1][j + 1]))
                    self.faces.append(Face(verts[i][j], verts[i + 1][j + 1], verts[i][j + 1]))

        # adding all vertices to the mesh-list
        for i in range(len(verts)):
            for j in range(len(verts[0])):
                self.vertices.append(verts[i][j])

    def compileModel(self, xrange, yrange, n, quad=False):
        """
        Generates the vertices and faces for the given parameters
        """
        lat = lattice(xrange, yrange, n)
        verts = self._mapVerts(lat)
        self._mapFaces(verts, quad)


class Torus(FromParametrisation):
    """
    Class for generating a mesh of a torus
    """
    def __init__(self, R=1, r=0.5, n=25, quad=True):
        """
        :param R: (float) the radius for the 'big' ring
        :param r: (float) the radius for the 'small' ring
        :param n: (int) see the documentation of the class 'FromParametrisation'
        :param quad: (bool)
        """
        self.R = R
        self.r = r

        super().__init__(self.torus, xrange=(0, 2 * math.pi), yrange=(0, 2 * math.pi), n=n, quad=quad)
        self.name = "Torus"

    def torus(self, x, y):
        x0 = (self.R + self.r * math.cos(y)) * math.cos(x)
        x1 = (self.R + self.r * math.cos(y)) * math.sin(x)
        x2 = self.r * math.sin(y)
        return x0, x1, x2


class TrefoilKnot(FromParametrisation):
    """
    Class for generating a mesh of a trefoil
    """
    def __init__(self, R=2, r=0.5, n=50, quad=False):
        """
        :param R: (float)
        :param r: (float)
        :param n:
        :param quad:
        """
        self.R = R
        self.r = r

        super().__init__(self.trefoil, xrange=(0, 12 * math.pi), yrange=(0, 2 * math.pi), n=n, quad=quad)
        self.name = "Trefoil"

    def trefoil(self, x, y):
        a = (self.R + self.r * math.cos(x / 2)) * math.cos(x / 3)
        b = (self.R + self.r * math.cos(x / 2)) * math.sin(x / 3)
        c = self.r + math.sin(x / 2)
        x0 = a + self.r * math.cos(x / 3) * math.cos(y - math.pi)
        x1 = b + self.r * math.sin(x / 3) * math.cos(y - math.pi)
        x2 = c + self.r * math.sin(y - math.pi)
        return x0, x1, x2


class KleinBottle(FromParametrisation):
    """
    Class for generating a mesh of a Klein bottle
    """
    def __init__(self, n=35, quad=True):
        super().__init__(self.klein, xrange=(0, math.pi), yrange=(0, 2 * math.pi), n=n, quad=quad)
        self.name = "Klein bottle"

    @staticmethod
    def klein(x, y):
        x0 = (-2 / 15) * math.cos(x) * (3 * math.cos(y) - 30 * math.sin(x) + 90 * pow(math.cos(x), 4) *
                                        math.sin(x) - 60 * pow(math.cos(x), 6) * math.sin(x) + 5 * math.cos(x) *
                                        math.cos(y) * math.sin(x))
        x1 = (-1 / 15) * math.sin(x) * (3 * math.cos(y) - 3 * pow(math.cos(x), 2) * math.cos(y) -
                                        48 * pow(math.cos(x), 4) * math.cos(y) + 48 * pow(math.cos(x), 6) *
                                        math.cos(y) - 60 * math.sin(x) + 5 * math.cos(x) * math.cos(y) * math.sin(x) -
                                        5 * pow(math.cos(x), 3) * math.cos(y) * math.sin(x) - 80 * pow(math.cos(x), 5) *
                                        math.cos(y) * math.sin(x) + 80 * pow(math.cos(x), 7) *
                                        math.cos(y) * math.sin(x))
        x2 = (2 / 15) * (3 + 5 * math.cos(x) * math.sin(x)) * math.sin(y)
        return x0, x1, x2


class MoebiusStrip(FromParametrisation):
    """
    Class for generating a mesh of a Moebius strip
    """
    def __init__(self, n=30, quad=True):
        super().__init__(self.moebius, xrange=(0, 2 * math.pi), yrange=(-1, 1), n=n, quad=quad)
        self.name = "Moebius strip"

    @staticmethod
    def moebius(x, y):
        x0 = math.cos(x) * (1 + (y / 2) * math.cos(x / 2))
        x1 = math.sin(x) * (1 + (y / 2) * math.cos(x / 2))
        x2 = (y / 2) * math.sin(x / 2)
        return x0, x1, x2


class Apple(FromParametrisation):
    """
    Class for generating a mesh of an apple
    """
    def __init__(self, n=50, quad=True):
        super().__init__(self.apple, xrange=(-math.pi, math.pi), yrange=(-math.pi, math.pi), n=n, quad=quad)
        self.name = "Apple"

    @staticmethod
    def apple(x, y):
        r1 = 5
        r2 = 4.8
        x0 = math.cos(x) * (r1 + r2 * math.cos(y)) + pow(y / math.pi, 20)
        x1 = math.sin(x) * (r1 + r2 * math.cos(y)) + 0.25 * math.cos(5 * x)
        x2 = -2.3 * math.log(1 - 0.3157 * y) + 6 * math.sin(y) + 2 * math.cos(y)
        return x0, x1, x2
