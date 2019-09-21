from PIL import Image, ImageCms
import ciede2000

class Convert16:
    debug = 0

    acolor = {
      "black":      (  0,  0,  0),
      "darkblue":   ( 29, 43, 83),
      "darkpurple": (126, 37, 83),
      "darkgreen":  (  0,135, 81),
      "brown":      (171, 82, 54),
      "darkgray":   ( 95, 87, 79),
      "lightgray":  (194,195,199),
      "white":      (255,241,232),
      "red":        (255,  0, 77),
      "orange":     (255,163,  0),
      "yellow":     (255,236, 39),
      "green":      (  0,228, 54),
      "blue":       ( 41,173,255),
      "indigo":     (131,118,156),
      "pink":       (255,119,168),
      "peach":      (255,204,170)
    }
    
    def __init__(self, infile):
      self.infile = infile
      self.debug  = 1
    
    def getpix(self, img):
      width, height = img.size
      img_pixels = []
      for y in range(height):
        for x in range(width):
          img_pixels.append(img.getpixel((x,y)))
    
      return img_pixels
    
    
    def show(self, img_pixels, width=32):
      i = 0
      for p in (img_pixels):
        if i % width == 0:
            print("")
        print(str(p) + " ", end="")
        i += 1
    
    def convert(self, outfile):
      img = Image.open(self.infile)
      
      if img.mode != "RGB":
        img = img.convert("RGB")
      
      #srgb_profile = ImageCms.createProfile("sRGB")
      #lab_profile  = ImageCms.createProfile("LAB")
      #rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
      #lab_img = ImageCms.applyTransform(img, rgb2lab_transform)
      #print(lab_img)
      
      #pixels = self.getpix(img)
      #self.show(pixels, 64)
      
      width, height = img.size
      
      count = 0
      output = Image.new("RGB", (width, height))
      for x in range(width):
        for y in range(height):
          count += 1
          rgb1 = img.getpixel((x, y))
          lab1 = ciede2000.rgb2lab(rgb1)
      
          results = []
          for k in Convert16.acolor:
            rgb2 = Convert16.acolor[k]
            lab2 = ciede2000.rgb2lab(rgb2)
            result = ciede2000.ciede2000(lab1, lab2)
            results.append({ "color": k, "result": result })
            if self.debug == 1:
              print("rgb1: %s, rgb2: %s : %s" % (rgb1, rgb2, result))
      
          results.sort(key=lambda x: x["result"])
          if self.debug == 1 and results[0]["color"] != "white":
            print(results[0])

          output.putpixel((x, y), Convert16.acolor[results[0]["color"]])
          #print("%d," % (count), end="")
      
      output.save(outfile, "PNG")




