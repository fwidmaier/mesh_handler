from linalg import Vector


class Camera:
    def __init__(self, position, lock, upGuide):
        self.position = position
        self.lock = lock  # origin relative to the camera
        self.upGuide = upGuide

        self.look = None
        self.right = None
        self.up = None
        self.zoom = 1
        self.update()

    def update(self, w_geometry=(800, 500)):
        """
        :param w_geometry: (tuple) root tk geometry
        :return:
        """
        if w_geometry is not None:
            try:
                self.zoom = min(w_geometry) / 2
            except Exception as _:
                raise Exception("w_geometry has to be a float tuple with 2 entries!")

        self.look = (self.lock - self.position).normalize()
        self.upGuide = self.upGuide.normalize()
        self.right = self.look.cross(self.upGuide)
        self.up = self.right.cross(self.look)

    def setPosition(self, newPosition):
        self.position = newPosition
        #self.upGuide = self.up
        self.update()

    def setLock(self, newLock):
        self.lock = newLock
        self.update()

    def project(self, v):
        """
        :param v: Vector
        :return: The screen coordinates of a 3 dimensional point
        """
        w = v - self.position
        d = (w - self.lock) * self.look
        if d < -0.0001:
            return None

        x = w * self.right
        y = w * self.up
        c = (2.5 * self.zoom) / (d + 0.0001)
        return Vector(x, y).scale(c).scale(2)


class Object:
    def __init__(self):
        self.lines = list()
        self.vertices = list()
        self.color = "white"

    def setColor(self, clr):
        self.color = clr

    def addLine(self, v1, v2):
        if (v1, v2) in self.lines or (v2, v1) in self.lines:
            return
        self.lines.append((v1, v2))

    def draw(self, scene, *args, **kwargs):
        for line in self.lines:
            scene.dLine(self.vertices[line[0]], self.vertices[line[1]], *args, **kwargs)
