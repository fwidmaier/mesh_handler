import math


class Vector:
    def __init__(self, *args):
        self.entries = args

    @property
    def dim(self):
        return len(self.entries)

    @property
    def mag(self):
        return math.sqrt(self * self)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def normalize(self):
        return self.scale(1/self.mag)

    def scale(self, c):
        return Vector(*[c * self[i] for i in range(self.dim)])

    def __repr__(self):
        return str(self.entries)

    def __getitem__(self, item):
        try:
            return self.entries[item]
        except Exception as e:
            raise e

    def __mul__(self, other):
        if self.dim != other.dim:
            raise Exception("Dimensions do not align!")
        return sum([self[i] * other[i] for i in range(self.dim)])

    def __add__(self, other):
        if self.dim != other.dim:
            raise Exception("Dimensions do not align!")
        return Vector(*[self[i] + other[i] for i in range(self.dim)])

    def __sub__(self, other):
        if self.dim != other.dim:
            raise Exception("Dimensions do not align!")
        return Vector(*[self[i] - other[i] for i in range(self.dim)])

    def __eq__(self, other):
        if self.dim != other.dim:
            return False

        a = [self[i] == other[i] for i in range(self.dim)]
        r = True
        for ai in a:
            r &= ai

        return r

    def cross(self, other):
        if self.dim != 3 or other.dim != 3:
            raise Exception("Dimensions do not align! (Must be 3)")
        x1 = self[1]*other[2] - self[2]*other[1]
        x2 = self[2]*other[0] - self[0]*other[2]
        x3 = self[0]*other[1] - self[1]*other[0]
        return Vector(x1, x2, x3)

    def rotate_z(self, alpha):
        c = math.cos(alpha)
        s = math.sin(alpha)
        x = self.x * c - self.y * s
        y = self.x * s + self.y * c
        return Vector(x, y, self.z)

    def rotate_n(self, alpha, n):
        c = math.cos(alpha)
        s = math.sin(alpha)
        x = (pow(n.x, 2) * (1 - c) + c)*self.x + \
            (n.x * n.y * (1 - c) - n.z*s)*self.y + (n.x * n.z * (1 - c) + n.y * s)*self.z
        y = (n.y * n.x * (1 - c) + n.z * s)*self.x + \
            (pow(n.y, 2) * (1 - c) + c)*self.y + (n.y * n.z * (1 - c) - n.x * s)*self.z
        z = (n.z * n.x * (1- c) - n.y * s)*self.x + \
            (n.z * n.y * (1 - c) + n.x * s)*self.y + (pow(n.z, 2)*(1 - c) + c)*self.z
        return Vector(x, y, z)
