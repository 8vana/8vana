from PIL import Image

class ImageLoader:
    debug = 0

    rgb_color = {
        "black":      (0,  0,  0),
        "darkblue":   (29, 43, 83),
        "darkpurple": (126, 37, 83),
        "darkgreen":  (0, 135, 81),
        "brown":      (171, 82, 54),
        "darkgray":   (95, 87, 79),
        "lightgray":  (194, 195, 199),
        "white":      (255, 241, 232),
        "red":        (255,  0, 77),
        "orange":     (255, 163,  0),
        "yellow":     (255, 236, 39),
        "green":      (0, 228, 54),
        "blue":       (41, 173, 255),
        "indigo":     (131, 118, 156),
        "pink":       (255, 119, 168),
        "peach":      (255, 204, 170)
    }

    color = {
        "black":      0,
        "darkblue":   1,
        "darkpurple": 2,
        "darkgreen":  3,
        "brown":      4,
        "darkgray":   5,
        "lightgray":  6,
        "white":      7,
        "red":        8,
        "orange":     9,
        "yellow":     10,
        "green":      11,
        "blue":       12,
        "indigo":     13,
        "pink":       14,
        "peach":      15
    }



    def __init__(self, infile):
        self.infile = infile
        self.width  = 0
        self.height = 0
        self.map    = []

    def judge(self, rgb):
        """
        rgbの配列からpyxelの色番号を特定する
        """
        result = 16
        for k in (ImageLoader.rgb_color):
            if (ImageLoader.rgb_color[k] == rgb):
                result = ImageLoader.color[k]
                break
        return result


    def getpix(self, img):
        width, height = img.size
        pixels = []
        for y in range(height):
            for x in range(width):
                rgb = img.getpixel((x, y))
                pixels.append(self.judge(rgb))
        return pixels


    def show(self, pixmap, width=32):
        i = 0
        for p in (pixmap):
            if i % width == 0:
                print("")
            print("%2d" % (p), end="")
            i += 1

    def get_size(self):
        return [self.width, self.height]

    def get_pixelmap(self):
        """
        pyxelのカラーインデックスのマップを返す
        """
        img = Image.open(self.infile)
        width, height = img.size
        self.width  = width
        self.height = height

        if img.mode != "RGB":
            img = img.convert("RGB")
        
        pixmap = self.getpix(img)
        self.map = pixmap
        return self.map


