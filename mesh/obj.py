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
