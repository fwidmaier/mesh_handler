from PIL import Image, ImageDraw
from render import Camera
from linalg import Vector


class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.im = Image.new("RGB", (self.width, self.height), "#3d3d3d")
        self.draw = ImageDraw.Draw(self.im)

        self.objects = list()
        self.camera = Camera(Vector(2.5, 2, 1), Vector(0, 0, 0), Vector(0, 0, -1))

    def addObject(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)

    def dLine(self, v1, v2, *args, **kwargs):
        sc = self.camera.project(v1)
        se = self.camera.project(v2)
        if sc is None or se is None:
            v1 = v1 - self.camera.lock - self.camera.position
            v2 = v2 - self.camera.lock - self.camera.position
            if sc is None and se is None:
                return

            if sc is None:
                v = v2 - v1
                t = -(v1 * self.camera.look) / (v * self.camera.look)
                sc = self.camera.project(v.scale(t) + v1 + self.camera.position + self.camera.lock)

            if se is None:
                v = v2 - v1
                t = -(v1 * self.camera.look) / (v * self.camera.look)
                se = self.camera.project(v.scale(t) + v1 + self.camera.position + self.camera.lock)
        self.draw.line([(sc.x + self.width / 2, sc.y + self.height / 2),
                        (se.x + self.width / 2, se.y + self.height / 2)], *args, **kwargs)

    def drawGrid(self):
        n = int((self.camera.position - self.camera.lock).mag) + 5
        # n = 10  # update n based on camera position
        # print(n)
        if n % 2 == 1:
            n += 1
        jj = int(n / 2)
        for i in range(1, n):
            self.dLine(Vector(i - jj, -jj, 0), Vector(i - jj, jj, 0), fill="#4f4f4f", width=1)
            self.dLine(Vector(-jj, i * 1 - jj, 0), Vector(jj, i - jj, 0), fill="#4f4f4f", width=1)

        self.dLine(Vector(-jj, 0, 0), Vector(jj, 0, 0), fill="#a30e42", width=2)  # x
        self.dLine(Vector(0, -jj, 0), Vector(0, jj, 0), fill="#8ed112", width=2)  # y
        # self.dLine(Vector(0, 0, 0), Vector(0, 0, 1), fill="#0960f7", width=2)  # z

    def render(self, showGrid=True):
        self.im = Image.new("RGB", (self.width, self.height), "#3d3d3d")
        self.draw = ImageDraw.Draw(self.im)
        if showGrid:
            self.drawGrid()

        for obj in self.objects:
            obj.draw(self, fill=obj.color, width=1)
