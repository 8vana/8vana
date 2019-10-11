import pyxel
import imageloader
import actor

BLACK = 0
DARK_BLUE = 1
DARK_PURPLE = 2
DARK_GREEN = 3
BROWN = 4
DARK_GRAY = 5
LIGHT_GRAY = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
GREEN = 11
BLUE = 12
INDIGO = 13
PINK = 14
PEACH = 15

class App:
    def __init__(self):
        pyxel.init(255, 255)
        self.x = 0
        self.time_begin = 1555749269.0

        self.icon = {}
        # ImageLoaderを利用したアイコンの登録
        self.icon["mihon"] = actor.Actor(20, 80)
        self.icon["mihon"].imageload("images/search1_8.png")
        self.icon["mihon2"] = actor.Actor(40, 80)
        self.icon["mihon2"].imageload("images/search2_8.png")
        #self.icon["mihon"].imageload("images/mihon.png")
        self.icon["arrow"] = actor.Actor(20, 40)
        self.icon["arrow"].imageload("images/arrow1_up_8.png")
        self.icon["arrow2"] = actor.Actor(40, 40)
        self.icon["arrow2"].imageload("images/arrow2_up_8.png")

        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width
        
        self.passed_seconds = pyxel.frame_count / 5

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, self.x + 3, 3, 9) # x1, y1, x2, y2, color
        
        # draw text data
        #for num in range(2, 200, 8):
        #    s = '%03d' % (num/8)
        #    pyxel.text( num,  num, s, (num/8)) # x, y, color

        # draw pixcel data
        #for num in range(0, 17, 1):
        #    s = '%03d' % (num)
        #    pyxel.text( (num * 15) + 2,  216, s, 2) # x, y, string, color

        #for num in range(0, 255, 1):
        #    pyxel.pix( num, 224, (num % 15)) # x, y, color

        pyxel.line(20,0,20,200,WHITE)
        pyxel.line(21,0,21,200,GREEN)
        pyxel.line(19,0,19,200,BLUE)
        self.icon["arrow"].put()
        self.icon["arrow2"].put()
        self.icon["mihon2"].put()
        self.icon["mihon"].put()
        
        now = self.time_begin + self.passed_seconds
        str  = "{:.1f}".format(now)
        pyxel.text(
            200,
            240,
            str,
            7)  # x, y, string, color

App()
