import Image, ImageDraw


def getheight(clust):
  if not clust.left: return 1  # leaf
  return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
  if not clust.left: return 0  #leaf
  return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendogram(clust, labels, filename='clusters.png'):
  h = getheight(clust) * 20
  w = 1200
  depth = getdepth(clust)

  scale = float(w - 280)/depth  # leave margin for text (blognames)

  img = Image.new('RGB', (w,h), (255, 255, 255))
  draw = ImageDraw.Draw(img)

  draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))

  drawnode(draw, clust, 10, (h/2), scale, labels)
  img.save(filename)


def drawnode(draw, clust, x, y, scale, labels):
  if clust.id < 0:  # inner node
    h1 = getheight(clust.left) * 20
    h2 = getheight(clust.right) * 20
    top = y - (h1 + h2)/2
    bottom = y + (h1 + h2)/2

    linelen = clust.distance * scale
    draw.line((x, top + h1/2, x, bottom - h2/2), fill=(255, 0, 0))
    draw.line((x, top + h1/2, x + linelen, top + h1/2), fill=(255, 0, 0))
    draw.line((x, bottom - h2/2, x + linelen, bottom - h2/2), fill=(255, 0, 0))

    drawnode(draw, clust.left, x + linelen, top + h1/2, scale, labels)
    drawnode(draw, clust.right, x + linelen, bottom - h2/2, scale, labels)
  else:
    draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def draw2d(data, labels, filename='clust2d.png'):
  img = Image.new('RGB', (2000, 2000), (255, 255, 255))
  draw = ImageDraw.Draw(img)
  for i in range(len(data)):
    x = (data[i][0] + 0.5) * 1000
    y = (data[i][1] + 0.5) * 1000
    draw.text((x, y), labels[i], (0, 0, 0))
  img.save(filename)
