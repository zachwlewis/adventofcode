# adventofcode.com
# Day 8
# https://adventofcode.com/2019/day/8

import common

class Image:
  def __init__(self, width: int, height:int):
    self.width = width
    self.height = height
    self.layers = []

  def layerLength(self) -> int:
    """The length of each layer in the image."""
    return self.width * self.height

  def layerCount(self) -> int:
    """The number of layers contained in the image."""
    return len(self.layers)

  def loadFile(self, path: str) -> bool:
    """Loads an image from a file path.

    Returns the success of the load operation."""
    if self.width == 0 or self.height == 0: return False
    stream = open(path, 'r')
    p_val = stream.read(1)
    p_idx = 0
    layer = []

    # Clear the existing image
    self.layers = []

    while p_val != '\n':
      layer.append(int(p_val))
      p_val = stream.read(1)
      p_idx += 1
      if p_idx == self.layerLength():
        self.layers.append(layer)
        layer = []
        p_idx = 0

    return True

  def checksum(self) -> int:
    """Calculates the image checksum."""
    minZeros = -1
    ck = -1
    for layer in self.layers:
      if minZeros == -1 or minZeros > layer.count(0):
        minZeros = layer.count(0)
        ck = layer.count(1) * layer.count(2)

    return ck

  def render(self) -> str:
    """Renders the image to a string."""
    processed = ['█'] * self.layerLength()
    buffer = ""

    for layer in reversed(self.layers):
      idx = 0
      for pixel in layer:
        if pixel == 0:
          processed[idx] = ' '
        elif pixel == 1:
          processed[idx] = '█'

        idx += 1

    idx = 0
    while len(processed):
      buffer += processed.pop(0)
      idx += 1
      if idx == self.width:
        buffer += '\n'
        idx = 0

    return buffer

IMG_PATH = common.getFilePath('input8.txt')
IMG_WIDTH = 25
IMG_HEIGHT = 6

i = Image(IMG_WIDTH, IMG_HEIGHT)
i.loadFile(IMG_PATH)
print(i.checksum())
print(i.render())