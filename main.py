import pyxel
import os
import argparse
from app1vana.modules.actor import Actor


parser = argparse.ArgumentParser(description='1vana')
parser.add_argument('-l','--log_time',
    help='このオプションは、ログ再生機能で利用することを想定されており、ログファイル先頭のリソース（最も古いログ）から時刻を取得し、開始時刻の基準値として利用します。このオプションを利用しない場合は、現在時刻が開始時刻として利用されます。',
    action="store_true")
args = parser.parse_args()

class App:
    number_of_mode = 2

    def __init__(self):
        pyxel.init(255, 255, caption="Welcome to 8vana")
        self.dir = os.path.dirname(os.path.abspath("__file__")) + "/"

        self.icon = {}
        self.icon["title"] = Actor(16, 16)
        self.icon["title"].set_size(224, 71)
        self.icon["title"].imageload(self.dir + "common/assets/8vana_logo_224_16_edit.png", 3) # dark_green

        self.count        = 0
        self.selected_app = 0

        # draw mouse cursor
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.selected_app = 99
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.selected_app = 99
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.count += 1
            self.selected_app = self.count % App.number_of_mode
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        self.icon["title"].put()
        pyxel.text(88, 60, "The visualization tool of", 0)
        pyxel.text(88, 68, "security incidents like retro games.", 0)

        pyxel.text(84, 132, "Push SPACE: Select mode", 7)
        pyxel.text(84, 140, "Push ENTER: Start 8vana", 7)
        if(self.selected_app == 0):
            pyxel.text(128, 152, "> 1vana", 7)
            pyxel.text(128, 160, "  2vana", 7)
        elif(self.selected_app == 1):
            pyxel.text(128, 152, "  1vana", 7)
            pyxel.text(128, 160, "> 2vana", 7)


app = App()


if(app.selected_app == 0):
    print("1vana")
    from app1vana.app import App1vana
    App1vana(args.log_time)
elif(app.selected_app == 1):
    print("2vana")
    from app2vana.app import App2vana
    from app2vana.util import Utility
    utility = Utility()
    App2vana(utility)




