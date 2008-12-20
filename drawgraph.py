import Image, ImageDraw
import layoutgraph

def drawnetwork(sol, people, links, filename='net.png'):
  img = Image.new('RGB', (400, 400), (255, 255, 255))
  draw = ImageDraw.Draw(img)

  loc = layoutgraph.solutiontodict(sol, people)

  # draw links
  for (a, b) in links:
    draw.line((loc[a], loc[b]), fill=(255, 0, 0))

  # draw people
  for name, p in loc.items():
    draw.text(p, name, (0, 0, 0))

  img.save(filename)


if __name__ == '__main__':
  import optimization
  domain = [(10, 370)] * (len(layoutgraph.People) * 2)
  f = layoutgraph.makecost(layoutgraph.People, layoutgraph.Links)
  s = optimization.annealingoptimize(domain, f, step=50, cool=0.99)
  print f(s)
  print s
  drawnetwork(s, layoutgraph.People, layoutgraph.Links) 
  print 'Wrote net.png'
