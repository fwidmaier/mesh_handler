from mesh import Mesh, Vertex, Face
import os


class OBJFile:
    """
    A simple class for writing .obj files
    """
    HEADER = "# OBJ File, Felix Widmaier 2021\n"

    @staticmethod
    def write(filename, mesh, name=None):
        """
        A method for writing a mesh to a .obj file
        :param filename: (str) the path to the file to write to
        :param mesh: (Mesh) the mesh to be written
        :param name: (str) -optional- to specify the name of the object in a
                    comment in the target file
        """
        file = open(filename, "w")
        mesh.update()
        ex = OBJFile.HEADER
        if name is not None:
            ex += f"# {name}\n"
        else:
            ex += f"# {mesh.name}\n"
        for v in mesh.vertices:
            ex += v.export
        for f in mesh.faces:
            ex += f.export
        file.write(ex)
        file.close()
        print(f"Written '{mesh.name}' to {filename} ({len(mesh.faces) + len(mesh.vertices) + 2} "
              f"lines, {os.path.getsize(filename)} bytes) == {len(mesh.faces)} faces/{len(mesh.vertices)} vertices")

    @staticmethod
    def read(filename, axis="xzy"):
        a_num = {"x": 0, "y": 1, "z": 2}
        assemble_verts = lambda sigma: lambda linf: [linf[int(sigma[i])] for i in range(len(sigma))]
        permute_axis = assemble_verts(str(a_num[axis[0]]) + str(a_num[axis[1]]) + str(a_num[axis[2]]))

        try:
            file = open(filename, "r")
            lines = file.readlines()
        except Exception as e:
            raise e

        m = Mesh()

        vId = lambda s: int(s.split("/")[0]) - 1
        try:
            for line in lines:
                if line == "\n":
                    continue
                linf = line.split()
                if linf[0] == "v":
                    m.vertices.append(Vertex(*permute_axis(list(map(float, linf[1:4:])))))
                elif linf[0] == "f":
                    m.faces.append(Face(*list(map(vId, linf[1::]))))
        except Exception as e:
            raise e

        # scale down
        mm = max([v.mag for v in m.vertices])
        for i in range(len(m.vertices)):
            m.vertices[i] = m.vertices[i].scale(1/mm)

        # configure lines for rendering
        m.conf_lines()

        print(f"Successfully read {filename} ({len(m.vertices)} vertices, {len(m.faces)} faces)")
        print(f"{len(m.lines)} lines to draw")
        return m
