import pyxel
import pyxel.pyxel_wrapper

### グローバル定数
### self.mapリストに格納されて描画されるオブジェクト
ROAD   = 0  # 通路
WALL   = 1  # 壁
BLOCK  = 2  # 壊せるブロック
O_GATE = 3  # ゲート  ※画像的には4で表示するよ
TEKI1   = 7  # 敵キャラ1
TEKI2   = 8  # 敵キャラ2
MYCHAR = 9  # 自キャラ

ITEM_U = [ 0,16,32,64,64,-1,-1, 0,48, 0,-1,-1,-1,-1,-1,-1,-1,96,144]
ITEM_V = [ 0, 0, 0, 0, 0,-1,-1,80,80,16,-1,-1,-1,-1,-1,-1,-1,80,80]

ITEMS = [9,0,1,2,3,7,8,17,18]

class App():
    def __init__(self):
        pyxel.init(432,260,title="ばくだんくんマップエディタ",fps=48)
        ### 横27マス（432ドット）×縦13マス（208ドット）。縦208ドット目以降は情報欄
        pyxel.load("bomb.pyxres")

        pyxel.mouse(True)
        self.setMap3()
        self.select_item = 2
        self.undo_list = []

        pyxel.run(self.update,self.draw)

    def update(self):
        ### マップの初期化（F1キー～F4キー）
        if pyxel.btnp(pyxel.KEY_F1):
            self.setMap1()
        elif pyxel.btnp(pyxel.KEY_F2):
            self.setMap2()
        elif pyxel.btnp(pyxel.KEY_F3):
            self.setMap3()
        elif pyxel.btnp(pyxel.KEY_F4):
            self.setMap4()
        ### マップの出力（Consoleにprintされます）
        elif pyxel.btnp(pyxel.KEY_F12):
            self.printMap()
        ### 選択アイテムの変更
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):  ## 左カーソルキーでITEM選択
            if self.select_item > 0:
                self.select_item -= 1
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):  ## 右カーソルキーでITEM選択
            if self.select_item < len(ITEMS) - 1:
                self.select_item += 1
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  ## マウスでITEM選択
            if pyxel.mouse_y > 208:
                x = (pyxel.mouse_x - 13) // 23
                if x >= 0 and x < len(ITEMS):
                    self.select_item = x

        ### マップ上にアイテムをセット！
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            if pyxel.mouse_x >= 0 and pyxel.mouse_x < 432 and pyxel.mouse_y >= 0 and pyxel.mouse_y < 208:
                x = pyxel.mouse_x // 16
                y = pyxel.mouse_y // 16
                ### UNDOリストの末尾に  [x,y,元の値,新しい値]  を追加
                self.flag = True
                rec1 = []
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    item_num = self.select_item
                else:
                    item_num = 1
                rec2 = [x,y,self.map[y][x],ITEMS[item_num]]
                if len(self.undo_list) > 0:
                    rec1 = self.undo_list[-1]
                    if rec1[0] != rec2[0] or rec1[1] != rec2[1] or rec1[3] != rec2[3]:
                        self.flag = True
                    else:
                        self.flag = False
                if self.flag and rec2[2] != rec2[3]:
                    self.undo_list.append(rec2)
                    self.map[y][x] = ITEMS[item_num]
                #print(self.undo_list)
        ### UNDO処理
        if pyxel.btnp(pyxel.KEY_Z) and len(self.undo_list) > 0:
            rec = self.undo_list.pop(-1)
            self.map[rec[1]][rec[0]] = rec[2]

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0,0,432,208,3)
        ### マップ表示
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                pyxel.blt(x*16,y*16,0,ITEM_U[self.map[y][x]],ITEM_V[self.map[y][x]],16,16,3)
        ### 選択欄の表示
        for i,item in enumerate(ITEMS):
            pyxel.rect(16+i*24,218,16,16,3)
            pyxel.blt(16+i*24,218,0,ITEM_U[item],ITEM_V[item],16,16,3)
            pyxel.rectb(13+self.select_item*24,215,22,22,10)
            pyxel.rectb(14+self.select_item*24,216,20,20,7)
            pyxel.rectb(15+self.select_item*24,217,18,18,7)
        ### 操作説明の表示
        pyxel.text(22,240,"[RIGHT]/[LEFT] or [Mouse Button] to Select ITEM",7)
        pyxel.text(246,214,"[Mouse Button] to Set ITEM on MAP",7)
        pyxel.text(246,224,"[Ctrl]+[Z] to UNDO MAP",7)
        pyxel.text(246,240,"[F1][F2][F3][F4] to Reset Template-MAP",7)
        pyxel.text(246,250,"[F12] to Write Data to file (stagedata.txt)",7)

    def setMap1(self):
        self.map = [
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
    def setMap2(self):
        self.map = [
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
             [1,9,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    def setMap3(self):
        self.map = [
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
             [1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    def setMap4(self):
        self.map = [
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
             [1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

    def printMap(self):
      with open("stagedata.txt", "w") as out:
        print("\n\n", file=out)
        for y in range(len(self.map)):
            print("                [",end="", file=out)
            for x in range(len(self.map[y])):
                if self.map[y][x] == 4:
                    print("3",end="", file=out)
                else:
                    print("{}".format(self.map[y][x]),end="", file=out)
                if x < len(self.map[y]) - 1:
                    print(",",end="", file=out)
            if y < len(self.map) - 1:
                print("],", file=out)
            else:
                print("]", file=out)
        print("\n\n", file=out)
App()

