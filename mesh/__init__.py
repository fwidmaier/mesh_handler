from render import Object
from linalg import Vector


class Vertex(Vector):
    """
    A class to model basic properties of a n-dimensional vertex
    """
    def __init__(self, *coords):
        """
        :param coords: (float) The various coordinates of the vertex
        """
        super().__init__(*coords)
        self.id = 0  # stores the line number - to reference it in the OBJ file

    @property
    def export(self):
        """
        :return: (str) Returns the vertex in OBJ-format
        """
        ex = "v"
        for c in self.entries:
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

    def __getitem__(self, item):
        try:
            return self.vertices[item]
        except Exception as e:
            raise e

    @property
    def export(self):
        """""
        :return: Returns the face in OBJ-format
        """
        ex = "f "
        for v in self.vertices:
            ex += " %d" % v.vId
        return ex + "\n"


class Mesh(Object):
    """
    Models the (abstract) concept of a mesh.
    """
    def __init__(self):
        super().__init__()
        self.faces = list()  # stores all faces of the mesh
        self.vertices = list()  # stores all vertices of the mesh
        self.name = "Object"

    @property
    def centroid(self):
        s = Vector(0, 0, 0)
        if len(self.vertices) == 0:
            return s

        for v in self.vertices:
            s = s + v
        return s.scale(1/len(self.vertices))

    def update(self):
        """
        A method to update all vertex-ids to reference them in a file
        """
        # update all vertex-ids
        for i, v in enumerate(self.vertices):
            v.id = i + 1

    def conf_lines(self):
        # configure lines for rendering
        aline = lambda id1, id2: self.addLine(face[id1], face[id2])
        for face in self.faces:
            if len(face.vertices) == 3:
                aline(0, 1)
                aline(1, 2)
                aline(2, 0)
            elif len(face.vertices) == 4:
                aline(0, 1)
                aline(1, 2)
                aline(2, 3)
                aline(3, 0)

    def translate(self, vec):  # vec is just an array of floats
        """
        just for development purposes
        """
        for i in range(len(self.vertices)):
            for j in range(len(vec)):
                self.vertices[i].coords[j] += vec[j]
