from requests import get  # Get images from online API
from io import BytesIO    # Image to Byte convertsion
from PIL import Image     # Image Manipulation
from time import time     # Time library
import math               # Math library

# This converts a latitude and longitude Into a tile number
def convert(lat, lon, z, extent = 1):
  z2 = 1 << z
  lon = ((lon + 180.0) % 360.0)
  lat = max(min(lat, 89.9), -89.9)
  lat_rad = math.radians(lat)
  zl_x = int(round(lon / (360.0 / (extent * z2))))
  zl_y = int(round(((extent * z2) / 2) * (1.0 - (math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi))))
  return [zl_x, zl_y]

# Get image from x/y tile
def getImg(xt, yt, z):
  # My API key - you can easily generate your own free one
  token = 'pk.eyJ1IjoicGJhcm4xMCIsImEiOiJja29neWRpa3kwdHNyMzBsYTMyZzY3Mjh2In0.4qncuUkuvlkh_AwRpz5pog'
  r = get(
    f'https://api.mapbox.com/v4/mapbox.satellite/{z}/{xt}/{yt}@2x.pngraw?access_token={token}',
    )
  return Image.open(BytesIO(r.content))

# Estimate time remaining using moving averages
def timeEst(s, t, p1, p2, xc, yc):
  if len(t) < 10:
    t.append(s)
  else:
    t.append(s)
    t.pop(0)

  print(f'Eta: {round(100*((sum(t)/len(t))*((abs(p1[0]-p2[0])*abs(p1[1]-p2[1])) -(xc*yc))))/100}')

def main(fn='out'):
  # two latitude/longitude coordinates
  p1, p2 = (
    (51.485556, -0.169958),
    (51.534091, -0.067033))
  # Zoom levels work on a logarthimic scale
  z = 15
  t = []
  # Generate the tile numbers
  p1, p2 = (
    convert(*p1, z),
    convert(*p2, z))
  # Iterate over the x/y tiles in a square
  # The square is formed to cover the two inputted points
  img = Image.new('RGB', (512*(abs(p1[0]-p2[0])+1), 512*(abs(p1[1]-p2[1])+1)))
  for xc,xt in enumerate(range(min(p1[0], p2[0]), max(p1[0], p2[0])+1)):
    for yc,yt in enumerate(range(min(p1[1], p2[1]), max(p1[1], p2[1])+1)):
      s = time()
      img.paste(getImg(xt, yt, z), (xc*512, yc*512))
      timeEst(time()-s, t, p1, p2, xc, yc)
  img.save(f'{fn}.png')
  
if __name__ == '__main__':
  main()
