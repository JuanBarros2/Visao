
import sys
from PIL import Image


def main(args):
    processImage(args[0])


def processImage(path):
    im = Image.open(path)
    print("Path:", path)
    print("Format:", im.format)
    print("Dimensions:", im.size)
    print("Mode:", im.mode)
    im.show()

    # split the image into individual bands
    source = im.split()
    R, G, B = 0, 1, 2

    mask = source[R].point(lambda i: i < 100 and 255)

    # process the green band
    out = source[G].point(lambda i: 0)

    # paste the processed band back, but only where red was < 100
    source[G].paste(out, None, mask)
    source[R].paste(out, None, mask)
    source[B].paste(out, None, mask)
    
    im = Image.merge(im.mode, source)
    im.show()

if __name__ == "__main__":
    main(sys.argv[1:])
