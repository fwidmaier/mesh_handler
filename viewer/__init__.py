import math
import time
from tkinter import *
from PIL import ImageTk
from render.scene import Scene
from linalg import Vector


class SceneView(Canvas):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.bind("<Configure>", self.on_resize)

        self.scene = Scene(self.width, self.height)
        img = ImageTk.PhotoImage(self.scene.im)
        self.panel = Label(self, image=img)
        self.panel.image = img
        self.panel.pack(side="bottom", fill="both", expand="yes")

    def on_resize(self, event):
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)
        self.scene.width = self.width
        self.scene.height = self.height

    def draw(self, showGrid=True):
        self.scene.render(showGrid)
        img = ImageTk.PhotoImage(self.scene.im)
        self.panel.configure(image=img)
        self.panel.image = img
        self.panel.update()
        self.panel.update_idletasks()
        self.update()
        self.update_idletasks()

    def addObject(self, obj):
        self.scene.addObject(obj)

    def setPosition(self, pos):
        self.scene.camera.setPosition(pos)

    def setTarget(self, target):
        self.scene.camera.setLock(target)


class Viewer(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x500")
        self.title("mesh view")
        self.frame = Frame(self)
        self.scene = SceneView(self.frame, highlightthickness=0)
        self.frame.pack(fill="both", expand="yes")
        self.scene.pack(fill="both", expand="yes")
        self.scene.addtag_all("all")
        self.scene.configure(bg="#3d3d3d")
        self.t = 0

        self.bind("<Button-4>", self.zoom_in)
        self.bind("<Button-5>", self.zoom_out)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<MouseWheel>", self.on_mousewheel)

        # mouse controls
        self.start_x = 0
        self.start_y = 0

    def update(self):
        self.scene.draw()
        #self.scene.scene.camera.setPosition(Vector(2 * math.cos(self.t * 0.01), 2 * math.sin(self.t * 0.01), 1))
        self.t += 1
        self.update_idletasks()
        self.scene.update_idletasks()

    def show(self):
        while True:
            try:
                self.update()
                time.sleep(0.001)
            except Exception as _:
                return

    def zoom_in(self, event):
        if (self.scene.scene.camera.position - self.scene.scene.camera.lock).mag > 0.05:
            self.scene.setPosition(self.scene.scene.camera.position + self.scene.scene.camera.look.scale(0.05))

    def zoom_out(self, event):
        self.scene.setPosition(self.scene.scene.camera.position + self.scene.scene.camera.look.scale(-0.05))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def rot_z(self, a):
        self.scene.scene.camera.upGuide = Vector(0,0,-1)
        self.scene.setPosition(self.scene.scene.camera.position.rotate_n(math.atan(a), Vector(0,0,1)))
        self.scene.scene.camera.upGuide = self.scene.scene.camera.up

    def rot_n(self, a):
        self.scene.setPosition(self.scene.scene.camera.position.rotate_n(
            math.atan(a),
            self.scene.scene.camera.right))
        self.scene.scene.camera.upGuide = self.scene.scene.camera.up

    def on_move_press(self, event):
        dx = self.start_x - event.x
        dy = self.start_y - event.y
        self.start_x = event.x
        self.start_y = event.y
        #a = self.scene.scene.camera.position.rotate_z(math.atan(-dx/500 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag))
        #a = a.rotate_n(math.atan(-dy/700 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag), self.scene.scene.camera.look.cross(self.scene.scene.camera.up))
        #self.scene.setPosition(self.scene.scene.camera.position.rotate_z(math.atan(-dx/500 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag)))
        #self.scene.setPosition(self.scene.scene.camera.position.rotate_n(math.atan(-dy/700 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag), self.scene.scene.camera.right))
        #self.scene.scene.camera.upGuide = self.scene.scene.camera.up
        self.rot_z(math.atan(-dx / 500 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag))
        self.rot_n(math.atan(-dy/700 * (self.scene.scene.camera.position - self.scene.scene.camera.look).mag))
        #self.scene.setPosition(a)

    def on_button_release(self, event):
        pass

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_in(None)
        else:
            self.zoom_out(None)