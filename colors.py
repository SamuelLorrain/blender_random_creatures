from random import uniform, sample, choice, random

def hsv_to_rgb(h,s,v):
    if s > 1 and v > 1:
        s = s * 0.01
        v = v * 0.01

    c = v * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r,g,b = (c,x,0)
    elif 60 <= h < 120:
        r,g,b = (x,c,0)
    elif 120 <= h < 180:
        r,g,b = (0,c,x)
    elif 180 <= h < 240:
        r,g,b = (0,x,c)
    elif 240 <= h < 300:
        r,g,b = (x,0,c)
    elif 300 <= h < 360:
        r,g,b = (c,0,x)

    return (round((r+m)*255), round((g+m)*255), round((b+m)*255))

def rgb_to_hsv(r,g,b):
    rp = r/255
    gp = g/255
    bp = b/255
    cmax = max(rp,gp,bp)
    cmin = min(rp,gp,bp)
    delta = cmax-cmin

    if delta == 0:
        h = 0
    elif cmax == rp:
        h = 60 * (((gp - bp)/delta) % 6)
    elif cmax == gp:
        h = 60 * (((bp - rp)/delta) + 2)
    elif cmax == bp:
        h = 60 * (((rp - gp)/delta) + 4)

    if cmax == 0:
        s = 0
    else:
        s = delta/cmax

    v = cmax

    return (h,s,v)


def hsl_to_rgb(h,s,l):
    c = (1 - abs((2 * l) - 1)) * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = l - (c/2)

    if 0 <= h < 60:
        r,g,b = (c,x,0)
    elif 60 <= h < 120:
        r,g,b = (x,c,0)
    elif 120 <= h < 180:
        r,g,b = (0,c,x)
    elif 180 <= h < 240:
        r,g,b = (0,x,c)
    elif 240 <= h < 300:
        r,g,b = (x,0,c)
    elif 300 <= h < 360:
        r,g,b = (c,0,x)

    return (round((r+m)*255), round((g+m)*255), round((b+m)*255))


def rgb_to_hsl(r,g, b):
    rp = r/255
    gp = g/255
    bp = b/255
    cmax = max(rp,gp,bp)
    cmin = min(rp,gp,bp)
    delta = cmax-cmin

    if delta == 0:
        h = 0
    elif cmax == rp:
        h = 60 * (((gp - bp)/delta) % 6)
    elif cmax == gp:
        h = 60 * (((bp - rp)/delta) + 2)
    elif cmax == bp:
        h = 60 * (((rp - gp)/delta) + 4)

    if delta == 0:
        s = 0
    else:
        s = delta/(1 - abs((2 * l) - 1))

    l = (cmax + cmin) / 2

    return (h,s,l)

"""
normalize value from
0 1 float range to 0 255 integer range
"""
def normalizeForFloatToWeb(value):
    return round(255/(value - 1) + 255)

"""
normalize value from
0 255 integer range to 0 1 float range
"""
def normalizeForWebToFloat(value):
    return round(1/(255 * (value - 255)) + 1)

"""
Generate random rgb color
"""
def generateRandomRgb(minR=0, maxR=255, minV=0, maxV=255, minB=0, maxB=255):
    return (
        choice(range(minR,maxR + 1)),
        choice(range(minV,maxV + 1)),
        choice(range(minB,maxB + 1))
    )

"""
Generate random rgb from hsv components
hue a un range de 0 à 360 (degrés)
saturation et value ont un range de 0 à 1
"""
def generateRandomRgbFromHsv(minH=0, maxH=360, minS=0, maxS=1, minV=0, maxV=1):
    return hsv_to_rgb(
        uniform(minH, maxH),
        uniform(minS, maxS),
        uniform(minV, maxV),
    )
"""
Generate random rgb from hls components
hue a un range de 0 à 360 (degrés)
light et saturation ont un range de 0 à 1
"""
def generateRandomRgbFromHsl(minH=0, maxH=360, minL=0, maxL=1, minS=0, maxS=1):
    return hls_to_rgb(
        uniform(minH, maxH),
        uniform(minL, maxL),
        uniform(minS, maxS),
    )


"""
Generate pastel RGB color
"""
def generatePastelRgb():
    return (
        round(random() * 127) + 127,
        round(random() * 127) + 127,
        round(random() * 127) + 127,
    )

"""
Blender uses (r,g,b,a) floating points colors
All values in the tuple goes from 0 to 1.
"""
def rgbToBlender(rgb):
    r,g,b = rgb
    return (
        r/256,
        g/256,
        b/256,
        1
    )

"""
Generate a new color by adding
rgb components and divide them by 2
"""
def addMixRgb(rgb1, rgb2):
        r1,g1,b1 = rgb1
        r2,g2,b2 = rgb2
        return (
            (r1 + r2) / 2,
            (g1 + g2) / 2,
            (b1 + b2) / 2,
        )

"""
Generate a new color by subbing
rgb components and multiply them by 2
"""
def subMixRgb(rgb1, rgb2):
        r1,g1,b1 = rgb1
        r2,g2,b2 = rgb2
        return (
            (r1 - r2) * 2,
            (g1 - g2) * 2,
            (b1 - b2) * 2,
        )

"""
Generate new color based on golden angle shift
http://en.wikipedia.org/wiki/Golden_angle
http://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
"""
def goldenRatioRgb(rgb, golden_ratio=137.508):
    hsv = rgb_to_hsv(*rgb)
    h,s,v = hsv
    h = (h + golden_ratio) % 360 # (hue + golden_ratio) % 360
    return hsv_to_rgb(h,s,v)

"""
Generate color theme based on a specific
algorithm
The "method" argument tell what algorithm to use
It takes 3 values:
- add
- sub
- gold (golden ratio)
"""
def generateColorSchemeRgb(rgb, numbers=5, method="gold"):
    colors = [rgb]
    for _ in range(0,numbers):
        if method == "add":
            colors.append(addMixRgb(rgb, generateRandomRgb()))
        elif method == "sub":
            colors.append(subMixRgb(rgb, generateRandomRgb()))
        elif method == "gold":
            colors.append(goldenRatioRgb(colors[-1]))

    return colors
