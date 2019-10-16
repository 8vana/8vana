class Util:
    def logger(self, m="", o="+"):
        print("[%s] %s" % (o, m))


    def chardump(self, charmap, width):
        """
        インデックスカラー形式のpngデータの1次元配列を指定された幅で改行して表示する
        """
        i = 0
        for p in charmap:
            if(i % width == 0):
                print()
            print("%2s" % (p), end=" ")
            i += 1
        print()