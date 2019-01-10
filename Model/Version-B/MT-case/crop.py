from PIL import Image

def cropImage(filename):
    im = Image.open(filename)
    left, top, right, bottom = 330, 70, 1600, 900
    im2 = im.crop((left, top, right, bottom))
    im2.save(filename)

for time in [80, 145, 200, 250, 300, 320, 350, 400, 450, 500, 575, 700]:
    filename = "t-%d.png" % time
    cropImage(filename)

