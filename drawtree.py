import Image, ImageDraw

def getwidth(tree):
  if tree.tb == None and tree.fb == None: return 1  # leaf
  return getwidth(tree.tb) + getwidth(tree.fb)


# XXX: why does `tree` have a value in this function?
#def getdepth(clust):
  #print tree
  #return 0

def getdepth(tree):
  if tree.tb == None and tree.fb == None: return 0  # leaf
  return max(getdepth(tree.tb), getdepth(tree.fb)) + 1


def drawtree(tree, png='tree.png'):
  w = getwidth(tree)*100
  h = getdepth(tree)*100 + 120

  img = Image.new('RGB', (w, h), (255, 255, 255))
  draw = ImageDraw.Draw(img)

  drawnode(draw, tree, w/2, 20)
  img.save(png, 'PNG')


def drawnode(draw, tree, x, y):

  if tree.results == None:  # internal node
    # Get width of each branch
    w1 = getwidth(tree.fb) * 100
    w2 = getwidth(tree.tb) * 100

    left = x - (w1 + w2)/2
    right = x + (w1 + w2)/2

    # Draw condition
    draw.text((x - 20, y - 10), '%s:%s' % (tree.col, tree.value), (0, 0, 0))

    # Draw links to branches
    draw.line((x, y, left + w1/2, y+100), fill=(255, 0, 0))
    draw.line((x, y, right - w2/2, y+100), fill=(255, 0, 0))
    
    drawnode(draw, tree.fb, left + w1/2, y + 100)
    drawnode(draw, tree.tb, right - w2/2, y + 100)
  else:
    txt = ' \n'.join(['%s:%d' % v for v in tree.results.items()])
    draw.text((x - 20, y), txt, (0, 0, 0))


if __name__ == '__main__':
  import treepredict
  tree = treepredict.buildtree(treepredict.testdata())
  drawtree(tree, 'tree.png')
  print 'Wrote tree.png'
