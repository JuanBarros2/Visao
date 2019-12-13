
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageMorph


def main(args):
    processImage(args[0])


def processImage(path):
    im = Image.open(path)
    print("Path:", path)
    print("Format:", im.format)
    print("Dimensions:", im.size)
    print("Mode:", im.mode)

    # Gerando níveis de dimensões diferentes
    dimensions = []
    # Utilizei potencias de dois por arbitrariedade mesmo
    for j in [2**i for i in range(5)]:
        dimensions.append((im.width / j, im.height / j))
        print(dimensions[-1])

    im_all = []
    for (width, height) in dimensions:
        aux = im.resize((int(width), int(height)))
        im_all.append(aux.resize((im.width, im.height)))
    
    map_char = []
    for im in im_all:
        for it in im_all:
            if im != it:
                map_char.append(ImageChops.difference(im, it))
    result = map_char[0] 
    for img in map_char[1:]:
        result = ImageChops.add(result, img, scale=2.0)
    # get an image

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', im.size, (255,255,255, 0))

    # get a font
    fnt = ImageFont.truetype('./Roboto-Black.ttf', 30)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    grayscale = result.convert('L')
    im = Image.open(path).convert('RGBA')
    out = im
    for i in range(1, 35):
        _, maxima = grayscale.getextrema()
        mask_image = grayscale.point(lambda i : 255 if i == maxima else 0)
        mask = ImageMorph.MorphOp(lut = ImageMorph.LutBuilder(patterns = ["1:(000 010 000)->1"]).build_lut())
        match = mask.match(mask_image)
        d.text(match[0], str(i), font=fnt, fill=(255,255,255,200))
        out = Image.alpha_composite(im, txt)
        supress = Image.new('L', (20, 20), "black")
        (w, h) = match[0]
        grayscale.paste(supress, (w-10, h-10))
    out.show()

if __name__ == "__main__":
    main(sys.argv[1:])
