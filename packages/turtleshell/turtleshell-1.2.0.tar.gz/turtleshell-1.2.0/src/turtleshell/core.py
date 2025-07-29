"""Convenience wrappers around turtle.Turtle and turtle.Screen
  See https://github.com/python/cpython/blob/main/Lib/turtle.py
  """
#TODO handle floats, randcoords, default screensize, default shape

import colorsys
from dataclasses import dataclass
import turtle

@dataclass
class HSV:
  hue: float
  sat: float
  val: float
  def __iter__(self):
    return iter(self.__dict__.values())

def Screen():
    """Return the singleton screen object."""
    if Turtle._screen is None:
        Turtle._screen = _Screen()
    return Turtle._screen

class _Screen(turtle._Screen):
  def __init__(self):
    super().__init__()
    turtle.TurtleScreen.__init__(self, _Screen._canvas)
    if turtle.Turtle._screen is None:
      turtle.Turtle._screen = self
    self.colormode(255)
  
  def _colorstr(self, color):
    isnumber = lambda x: isinstance(x, (int, float))
    if len(color) == 3 and all([isnumber(c) for c in color]):
      lower, upper = 0, Turtle._screen.colormode()
      color = [max(min(upper, round(c)), lower) for c in color]
    return super()._colorstr(color)

def _hsv_to_rgb(hsv):
  rgb = colorsys.hsv_to_rgb(*hsv)
  return [round(c*Turtle._screen.colormode()) for c in rgb]

class Turtle(turtle.RawTurtle):

  _pen = None
  _screen = None
  MULT = 20

  def __init__(self,
              shape=turtle._CFG["shape"],
              undobuffersize=turtle._CFG["undobuffersize"],
              visible=turtle._CFG["visible"]):
    if Turtle._screen is None:
      Turtle._screen = Screen()
    turtle.RawTurtle.__init__(self, Turtle._screen,
                        shape=shape,
                        undobuffersize=undobuffersize,
                        visible=visible)
    self.shapesize(Turtle.MULT)
    self._pen_hsv = HSV(0, 1, 1)
    self._fill_hsv = HSV(0, 1, 1)

  @property
  def x(self):
    return self.xcor()

  @x.setter
  def x(self, value):
    self.setx(value)

  @property
  def y(self):
    return self.ycor()

  @y.setter
  def y(self, value):
    self.sety(value)

  def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):

    if stretch_wid is None and stretch_len is None and outline is None:
      stretch_wid, stretch_len, outline = super().shapesize()
      return stretch_wid*Turtle.MULT, stretch_len*Turtle.MULT, outline

    stretch_wid = stretch_wid/Turtle.MULT if stretch_wid else None
    stretch_len = stretch_len/Turtle.MULT if stretch_len else None
    ret = super().shapesize(stretch_wid, stretch_len, outline)
    return ret

  def teleport(self, x, y):
    pendown = self.isdown()
    if pendown:
      self.pen(pendown=False)
    self.penup()
    self._position = turtle.Vec2D(x, y)
    self.pen(pendown=pendown)

  def write(self, arg, move=False, align="center", font=("Arial", 18, "bold")):
    super().write(arg, move, align, font)

  def to_front(self):
    self.goto(self.position())

  ## HSV colour methods
  def hue(self, degrees):
    self.penhue(degrees)
    self.fillhue(degrees)

  def penhue(self, degrees):
    self._pen_hsv.hue = degrees/360
    self.pencolor(_hsv_to_rgb(self._pen_hsv))

  def fillhue(self, degrees):
    self._fill_hsv.hue = degrees/360
    self.fillcolor(_hsv_to_rgb(self._fill_hsv))

  def sat(self, value):
    self.pensat(value)
    self.fillsat(value)

  def pensat(self, value):
    self._pen_hsv.sat = value/100
    self.pencolor(_hsv_to_rgb(self._pen_hsv))

  def fillsat(self, value):
    self._fill_hsv.sat = value/100
    self.fillcolor(_hsv_to_rgb(self._fill_hsv))

  def val(self, value):
    self.penval(value)
    self.fillval(value)

  def penval(self, value):
    self._pen_hsv.val = value/100
    self.pencolor(_hsv_to_rgb(self._pen_hsv))

  def fillval(self, value):
    self._fill_hsv.val = value/100
    self.fillcolor(_hsv_to_rgb(self._fill_hsv))


Pen = Turtle

if __name__ == "__main__":
  canvas = Screen()
  canvas.bgcolor("gold")
  pen = Turtle()
  print(f"\n\n***\nTURTLE TYPE: {type(pen)}\nSCREEN TYPE: {type(canvas)}\n***\n")

  pen.shape("square")
  pen.shapesize(30, 25)

  pen.hue(0)
  pen.stamp()
  pen.forward(50)
  pen.hue(60)
  pen.stamp()
  pen.forward(50)
  pen.hue(120)
  pen.stamp()
  pen.forward(50)
  pen.hue(180)
  pen.stamp()
  pen.forward(50)
  pen.hue(240)
  pen.stamp()

  canvas.exitonclick()