from tkinter import TclError       # Detect when window destroyed
from requests import get           # Get images from online API
from graphics import Gui           # Gui object
from PIL import Image              # Image object
from io import BytesIO             # Image to bytes conversion
import math                        # Math library

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
def getImg(xt, yt, z, rf):
    # My API key - you can easily generate your own free one
    token = 'pk.eyJ1IjoicGJhcm4xMCIsImEiOiJja29neWRpa3kwdHNyMzBsYTMyZzY3Mjh2In0.4qncuUkuvlkh_AwRpz5pog'
    r = get(
        f'https://api.mapbox.com/v4/mapbox.satellite/{z}/{xt}/{yt}@2x.pngraw?access_token={token}',
        )
    img = Image.open(BytesIO(r.content))
    img = img.resize((512//(2**rf),512//(2**rf)))
    img.save('temp.png')

def update():
    global zoom, lat, lon, g, od

    for zc in range(3):
        z = zoom + zc
        it = 2**(zc)

        xt, yt = convert(lat, lon, math.ceil(z))
        xt = math.ceil(xt/it)*it
        yt = math.ceil(yt/it)*it
        for x in range(math.ceil(g.root.winfo_width()/(512//(2**zc)))):
            for y in range(math.ceil(g.root.winfo_height()/(512//(2**zc)))):
                # Check for update to exit
                cd = [g.root.winfo_width(), g.root.winfo_height(), lat, lon]
                if od != cd:
                    od = cd
                    return

                xta = xt + x
                yta = yt + y
                getImg(xta, yta, z, zc)
                g.addImg(x*(512//(2**zc)), y*(512//(2**zc)))
                g.upd()

def main():
    global zoom, lat, lon, g, od

    g = Gui()

    zoom, lat, lon = 12, 51.410008, -0.103875
    od = [600, 600, lat, lon] # OLD DATA width, height, x, y

    while 1:
        cd = [g.root.winfo_width(), g.root.winfo_height(), lat, lon]
        if od != cd:
            od = cd
            update()
        else:
            g.upd()
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        if type(e) != TclError:
            raise