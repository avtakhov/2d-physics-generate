import tkinter
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Constant(tkinter.Frame):
    def __init__(self, name):
        super().__init__()
        self.label = tkinter.Label(text=name)
        self.entry = tkinter.Entry()
        self.value = 0
        self.name = name
        self.draw()

    def draw(self):
        self.label.pack()
        self.entry.pack()

    def read(self):
        self.value = float(self.entry.get())


class Constants(tkinter.Frame):
    def __init__(self):
        super().__init__()
        self.v = Constant("v")
        self.d = Constant("d")
        self.a = Constant("a")
        self.window = None

    def read(self):
        self.v.read()
        self.d.read()
        self.a.read()

    def get(self, time):
        if self.a.value == 0:
            return Point(self.d.value, -self.v.value * time)
        else:
            return Point(
                self.d.value * math.cos(self.a.value * time),
                -self.v.value / self.a.value * math.sin(time * self.a.value))


class Cartesian(tkinter.Frame):

    def __init__(self, zx, zy):
        super().__init__()
        self.constants = Constants()
        self.ZERO = Point(zx, zy)
        self.canvas = tkinter.Canvas(self)
        self.line_size = 300
        self.start = tkinter.Button(text="start", command=self.action)
        self.draw()

    def draw(self):
        self.pack(fill=tkinter.BOTH, expand=1)
        self.canvas.create_line(self.ZERO.x - self.line_size, self.ZERO.y, self.ZERO.x + self.line_size, self.ZERO.y)
        self.canvas.create_line(self.ZERO.x, self.ZERO.y - self.line_size, self.ZERO.x, self.ZERO.y + self.line_size)
        self.start.pack()
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

    def action(self):
        self.constants.read()
        t = 0
        dt = 0.001
        while True:
            pt = self.constants.get(t)
            x = self.ZERO.x + pt.x
            y = self.ZERO.y + pt.y
            self.canvas.create_oval(x, y, x, y)
            self.canvas.update_idletasks()
            self.canvas.update()
            t += dt


def main():
    root = tkinter.Tk()
    c = Cartesian(300, 300)
    root.geometry("1500x900")
    root.mainloop()


if __name__ == "__main__":
    main()
