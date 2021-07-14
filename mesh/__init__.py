from abc import ABC
from mesh.obj import *


class Vertex:
    """
    A class to model basic properties of a n-dimensional vertex
    """
    def __init__(self, *coords):
        """
        :param coords: (float) The various coordinates of the vertex
        """
        self.coords = list(coords)  # stores the coordinates
        self.id = 0  # stores the line number - to reference it in the OBJ file

    @property
    def export(self):
        """
        :return: (str) Returns the vertex in OBJ-format
        """
        ex = "v"
        for c in self.coords:
            ex += " %.5f" % c  # precision is set to 5 decimal places
        return ex + "\n"

    @property
    def vId(self):
        """
        :return: (int) A fancy way to obtain the id of the vertex
        """
        return self.id


class Face:
    """
    A class to model basic properties of a face
    """
    def __init__(self, *verts):
        """
        :param verts: (Vertex) All the vertices that make up the face
        """
        self.vertices = verts

    @property
    def export(self):
        """""
        :return: Returns the face in OBJ-format
        """
        ex = "f "
        for v in self.vertices:
            ex += " %d" % v.vId
        return ex + "\n"


class Mesh(ABC):
    """
    Models the (abstract) concept of a mesh.
    """
    def __init__(self):
        self.faces = list()  # stores all faces of the mesh
        self.vertices = list()  # stores all vertices of the mesh
        self.name = "Object"

    def update(self):
        """
        A method to update all vertex-ids to reference them in a file
        """
        # update all vertex-ids
        for i, v in enumerate(self.vertices):
            v.id = i + 1

    def translate(self, vec):  # vec is just an array of floats
        """
        just for development purposes
        """
        for i in range(len(self.vertices)):
            for j in range(len(vec)):
                self.vertices[i].coords[j] += vec[j]
