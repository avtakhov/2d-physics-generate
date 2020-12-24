import tkinter
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, canvas, x, y, height, width, fill):
        self.canvas = canvas
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.rect = canvas.create_rectangle(x, y, x + width, y - height, fill=fill)

    def __update(self):
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y - self.height)

    def mouse(self, event):
        self.move(event.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.__update()


class SystemState:
    def __init__(self, x, y):
        self.c1 = 0
        self.c2 = 0
        self.c3 = 0
        self.c4 = 0
        self.update(x, y)

    def get(self, t):
        c = [0, self.c1, self.c2, self.c3, self.c4]
        x1 = c[1] * math.cos(t) + c[2] * math.sin(t) + c[3] * math.cos(t / math.sqrt(6)) + c[4] * math.sin(
            t / math.sqrt(6))
        x2 = -c[1] * math.cos(t) - c[2] * math.sin(t) + 3 / 2 * c[3] * math.cos(t / math.sqrt(6)) + 3 / 2 * c[4] \
             * math.sin(t / math.sqrt(6))
        return x1, x2

    def update(self, x1, x2):
        self.c1 = (3 * x1 - 2 * x2) / 5
        self.c3 = 2 * (x1 + x2) / 5


class Cartesian(tkinter.Frame):

    def __init__(self, zx, zy):
        super().__init__()
        self.ZERO = Point(zx, zy)
        self.canvas = tkinter.Canvas(self)
        self.line_size = 600
        self.draw()
        self.LEFT_ZERO = self.ZERO.x + 150
        self.RIGHT_ZERO = self.ZERO.x + 300
        self.left_rect = Rectangle(self.canvas, self.LEFT_ZERO, self.ZERO.y, 30, 50, "yellow")
        self.right_rect = Rectangle(self.canvas, self.RIGHT_ZERO, self.ZERO.y, 30, 50, "purple")
        self.state = SystemState(0, 0)
        self.canvas.bind('<B1-Motion>', self.mouse)
        self.canvas.bind('<ButtonRelease-1>', self.state_update)
        self.continue_action = True
        self.count = 10
        self.lsticks = [(self.canvas.create_line(0, 0, 0, 0),
                         self.canvas.create_line(0, 0, 0, 0)) for i in range(self.count)]
        self.rsticks = [(self.canvas.create_line(0, 0, 0, 0),
                         self.canvas.create_line(0, 0, 0, 0)) for i in range(self.count)]
        self.stick_update()
        self.time = 0

    def mouse(self, event):
        self.continue_action = False
        self.right_rect.mouse(event)
        self.left_rect.move(self.ZERO.x + (self.right_rect.x - self.ZERO.x) // 2 - self.left_rect.width // 2,
                            self.left_rect.y)
        self.stick_update()

    def state_update(self, event):
        self.state.update(self.left_rect.x - self.LEFT_ZERO, self.right_rect.x - self.RIGHT_ZERO)
        self.continue_action = True
        self.time = 0

    def draw(self):
        self.pack(fill=tkinter.BOTH, expand=1)
        self.canvas.create_line(self.ZERO.x - self.line_size, self.ZERO.y, self.ZERO.x + self.line_size, self.ZERO.y)
        self.canvas.create_line(self.ZERO.x, self.ZERO.y - self.line_size, self.ZERO.x, self.ZERO.y)
        self.canvas.pack(fill=tkinter.BOTH, expand=1)

    def sticks(self, l, r, old):
        if l > r:
            l, r = r, l
        h = [l + i * (r - l) // self.count for i in range(self.count + 1)]
        for i in range(1, len(h)):
            self.canvas.coords(old[i - 1][0], h[i], self.ZERO.y - 20, h[i], self.ZERO.y - 5)
            self.canvas.coords(old[i - 1][1], h[i - 1], self.ZERO.y - 20, h[i], self.ZERO.y - 5)

    def stick_update(self):
        self.sticks(self.ZERO.x, self.left_rect.x, self.lsticks)
        self.sticks(self.left_rect.x + self.left_rect.width, self.right_rect.x, self.rsticks)

    def action(self):
        dt = 0.01
        while True:
            if self.continue_action:
                x1, x2 = self.state.get(self.time)
                self.left_rect.move(self.LEFT_ZERO + x1, self.ZERO.y)
                self.right_rect.move(self.RIGHT_ZERO + x2, self.ZERO.y)
            self.stick_update()
            self.time += dt

            self.canvas.update_idletasks()
            self.canvas.update()


def main():
    root = tkinter.Tk()
    c = Cartesian(300, 300)
    root.geometry("1500x900")
    c.action()
    root.mainloop()


if __name__ == "__main__":
    main()
