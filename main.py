import tkinter
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Constant(tkinter.Frame):
    def __init__(self, name, default=0):
        super().__init__()
        self.label = tkinter.Label(text=name)
        self.entry = tkinter.Entry()
        self.entry.insert(tkinter.END, str(default))
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
        self.a = Constant("a", 1)
        self.c = [Constant(f'C{i}', 20) for i in range(1, 5)]
        self.c.insert(0, None)

    def read(self):
        self.a.read()
        for i in self.c:
            if i is not None:
                i.read()

    def get(self, t):
        c = [0] + [self.c[i].value for i in range(1, 5)]
        a = self.a.value
        x1 = c[1] * math.cos(a * t) + c[2] * math.sin(a * t) + c[3] * math.cos(a * t / math.sqrt(6)) + c[4] * math.sin(
            a * t / math.sqrt(6))
        x2 = -c[1] * math.cos(a * t) - c[2] * math.sin(a * t) + 3 / 2 * c[3] * math.cos(a * t / math.sqrt(6)) + 3 / 2 * \
             c[4] * math.sin(a * t / math.sqrt(6))
        return x1, x2


class Cartesian(tkinter.Frame):

    def __init__(self, zx, zy):
        super().__init__()
        self.constants = Constants()
        self.start = tkinter.Button(text="start", command=self.action)
        self.ZERO = Point(zx, zy)
        self.canvas = tkinter.Canvas(self)
        self.line_size = 600
        self.draw()

    def draw(self):
        self.start.pack()
        self.pack(fill=tkinter.BOTH, expand=1)
        self.canvas.create_line(self.ZERO.x - self.line_size, self.ZERO.y, self.ZERO.x + self.line_size, self.ZERO.y)
        self.canvas.create_line(self.ZERO.x, self.ZERO.y - self.line_size, self.ZERO.x, self.ZERO.y)
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

    def print_sticks(self, x1, x2, count, size):
        step = (x2 - x1) / count
        cur = x1
        for i in range(count):
            nxt = cur + step
            self.canvas.create_line(nxt, self.ZERO.y - 5, nxt, self.ZERO.y - size + 5, tag='action')
            self.canvas.create_line(cur, self.ZERO.y - 5, nxt, self.ZERO.y - size + 5, tag='action')
            cur = nxt

    def action(self):
        self.constants.read()
        t = 0
        dt = 0.01
        size = 30
        stick_number = 10
        sx1 = self.ZERO.x + 150
        sx2 = self.ZERO.x + 300
        delete = False
        while True:
            x1, x2 = self.constants.get(t)
            if delete:
                self.canvas.delete('action')
            l1 = sx1 + x1 - size
            r1 = sx1 + x1 + size

            l2 = sx2 + x2 - size
            r2 = sx2 + x2 + size

            self.canvas.create_rectangle(l1, self.ZERO.y, r1, self.ZERO.y - size,
                                         fill='yellow', tag="action")
            self.canvas.create_rectangle(l2, self.ZERO.y, r2, self.ZERO.y - size,
                                         fill='green', tag="action")
            self.print_sticks(self.ZERO.x, l1, stick_number, size)
            self.print_sticks(r1, l2, stick_number, size)
            delete = True
            t += dt
            self.canvas.update_idletasks()
            self.canvas.update()


def main():
    root = tkinter.Tk()
    Cartesian(300, 300)
    root.geometry("1500x900")
    root.mainloop()


if __name__ == "__main__":
    main()
