# adventofcode.com
# Day 8
# https://adventofcode.com/2019/day/8

import common

IMG_WIDTH = 25
IMG_HEIGHT = 6
LAYER_SIZE = IMG_WIDTH * IMG_HEIGHT

f = open(common.getFilePath('input8.txt'), 'r')
img = []
i = f.read(1)
while i != '\n':
  img.append(int(i))
  i = f.read(1)

def parseImage(input, width, height):
  layer_length = width * height
  image = []
  layer = []
  count = 0

  for pixel in input:
    layer.append(pixel)
    count += 1

    if count == LAYER_SIZE:
      image.append(layer)
      layer = []
      count = 0

  return image


def checksum(image):
  layers = []
  counts = []
  layer = []
  count = 0
  number_count = dict()

  for pixel in image:
    layer.append(pixel)
    number_count.setdefault(pixel, 0)
    number_count[pixel] += 1
    count += 1
    if count == LAYER_SIZE:
      layers.append(layer)
      counts.append(number_count)
      layer = []
      number_count = dict()
      count = 0

  zeros = 1000000
  value = 0
  for values in counts:
    if values[0] < zeros:
      zeros = values[0]
      value = values[1] * values[2]

  return value

def processImage(image, width, height):
  im = list(image)
  im.reverse()
  processed = im[0]
  
  for layer in im:
    pid = 0
    for pixel in layer:
      if pixel == 0: processed[pid] = ' '
      elif pixel == 1: processed[pid] = '█' #░█
      pid += 1

  s = ""
  col = 0
  while len(processed):
    s += processed.pop(0)
    col += 1
    if col == width:
      col = 0
      s += '\n'

  return s

print(checksum(img))
print(processImage(parseImage(img, IMG_WIDTH, IMG_HEIGHT), IMG_WIDTH, IMG_HEIGHT))