import pyxel
import math

### self.mapリストに格納されて描画されるオブジェクト
ROAD   = 0  # 通路
WALL   = 1  # 壁
BLOCK  = 2  # 壊せるブロック
C_GATE = 3  # ゲート（隠れてる状態）
O_GATE = 4  # ゲート（オープン状態）
ITEM_MAXUP = 5  # アイテム（爆弾数UP）
ITEM_LENUP = 6  # アイテム（爆弾威力UP）
BROKENBLK  = 10  # 燃えかけの壊せるブロック
EXPLO  = 11  # 爆発
### self.mapリストに格納されるが別で描画するオブジェクト
BOMB   = 15  # 爆弾
### self.mapリストには格納しないオブジェクト
TEKI1   = 7  # 敵キャラ1
TEKI2   = 8  # 敵キャラ2
MYCHAR = 9  # 自キャラ
### グローバル変数（定数）
D = [[0,1],[0,-1],[1,0],[-1,0]]

class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moving = False
        self.dir = 0

class MyChar(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bomb_max = 1
        self.bomb_len = 1

    def update(self, map):
        if self.moving:
            self.x += D[self.dir][0] * 2
            self.y += D[self.dir][1] * 2
            pyxel.play(0,pyxel.sounds[3])
        if self.x % 16 == 0 and self.y % 16 == 0:
            self.moving = False

    def draw(self):
        n1 = self.dir * 16
        n2 = 0
        if self.moving:
            n2 = ( pyxel.frame_count % 4 ) * 16
        pyxel.blt(self.x,self.y,0,n2,16+n1,16,16,3)
        #print("{} {}".format(self.bomb_max,self.bomb_len))

class Teki1(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, map):
        if self.moving:
            self.x += D[self.dir][0]
            self.y += D[self.dir][1]
        if self.x % 16 == 0 and self.y % 16 == 0:
            self.moving = False
            x = int(self.x / 16)
            y = int(self.y / 16)
            n = pyxel.rndi(0,3)
            for i in range(4):
                obj = map[y + D[(n+i)%4][1]][x + D[(n+i)%4][0]]
                if obj == ROAD or obj == O_GATE:
                    self.dir = (n+i)%4
                    self.moving = True
                    break

    def draw(self):
        n = ( round( (pyxel.frame_count + self.x) / 6) % 3 ) * 16
        pyxel.blt(self.x,self.y,0,n,80,16,16,3)

class Teki2(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.baisuu = 1

    def update(self, map):
        if self.moving:
            self.x += D[self.dir][0] * self.baisuu
            self.y += D[self.dir][1] * self.baisuu
        if self.x % 16 == 0 and self.y % 16 == 0:
            self.moving = False
            if pyxel.frame_count//120%3 == 0:
                self.baisuu = 2
            else:
                self.baisuu = 1
            x = int(self.x / 16)
            y = int(self.y / 16)
            n = pyxel.rndi(0,3)
            for i in range(4):
                obj = map[y + D[(n+i)%4][1]][x + D[(n+i)%4][0]]
                if obj == ROAD or obj == O_GATE:
                    self.dir = (n+i)%4
                    self.moving = True
                    break

    def draw(self):
        n = ( round( (pyxel.frame_count + self.x) / 6) % 3 ) * 16
        pyxel.blt(self.x,self.y,0,48 + n,80,16,16,3)

class Bomb(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.count = 72

    def update(self):
        self.count -= 1

    def draw(self):
        n = (4 - math.floor(self.count / 18)) * 16
        pyxel.blt(self.x,self.y,0,n,96,16,16,3)
    
class Message(Sprite):
    def __init__(self, x, y, message):
        super().__init__(x, y)
        self.count = 40
        self.message = message
    def update(self):
        self.count -= 1
        self.y -= 0.2
    def draw(self):
        pyxel.text(self.x,self.y,self.message,7)

class App():
    def __init__(self):
        pyxel.init(272,238,title="ばくだんくん",fps=48)
        pyxel.load("bomb.pyxres")

        self.init_game()

        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.stage_num = 0
        self.score = 0
        self.my_char = MyChar(16,16)
        self.KEY = [pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
        self.gameclear_flag = False
        self.showtitle_flag = True
        self.showtitle_counter = 0
        self.gameover_flag = False
        return

    def init_stage(self):
        self.tekis = []
        self.bombs = []
        self.messages = []
        self.left_time = 48 * 300
        self.stageclear_flag = True
        #pyxel.play(0,pyxel.sounds[1])
        pyxel.play(0,pyxel.sounds[10])
        self.stageclear_counter = 160
        self.map = []
        self.setMap()
        if len(self.map) == 0:
            self.gameclear_flag = True
            self.gameclear_counter = 360
            pyxel.play(0,pyxel.sounds[13])
            return
        for y in range(0,13):
            for x in range(0,17):
                if self.map[y][x] == MYCHAR:
                    self.my_char.x = x*16
                    self.my_char.y = y*16
                    self.my_char.dir = 0
                    self.map[y][x] = ROAD
                elif self.map[y][x] == TEKI1:
                    self.tekis.append(Teki1(x*16,y*16))
                    self.map[y][x] = ROAD
                elif self.map[y][x] == TEKI2:
                    self.tekis.append(Teki2(x*16,y*16))
                    self.map[y][x] = ROAD

    def update(self):
        ### タイトル画面表示状態の処理
        if self.showtitle_flag:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.showtitle_counter = 48
                pyxel.play(0,pyxel.sounds[7])
            elif self.showtitle_counter > 0:
                self.showtitle_counter -= 1
                if self.showtitle_counter == 0:
                    self.showtitle_flag = False
                    self.init_stage()
            return
        ### ゲームオーバー後の処理
        if self.gameover_flag == True:
            self.gameover_counter -= 1
            if self.gameover_counter < 0:
                self.init_game()
        else:
            self.left_time -= 1
            if self.left_time == 0:
                    self.gameover_flag = True
                    pyxel.play(1,pyxel.sounds[5])
                    self.gameover_counter = 120
                    return
        ### ゲームクリア後の処理
        if self.gameclear_flag == True:
            self.gameclear_counter -= 1
            if self.gameclear_counter < 0:
                self.init_game()
            return
        ### ステージ更新処理中の処理
        if self.stageclear_flag == True:
            self.stageclear_counter -= 1
            if self.stageclear_counter < 0:
                self.stageclear_flag = False
            return
        ### 残り時間を減らす
        ### キーボード入力の判定
        if self.my_char.moving == False  and self.gameover_flag == False:
            ### カーソルキーの判定　：自キャラを移動
            for i in range(4):
                if pyxel.btn(self.KEY[i]):
                    x = int(self.my_char.x/16) + D[i][0]
                    y = int(self.my_char.y/16) + D[i][1]
                    obj = self.map[y][x]
                    if  obj==ROAD or obj==O_GATE or obj==ITEM_MAXUP or obj==ITEM_LENUP:
                        self.my_char.dir = i
                        self.my_char.moving = True
                        if obj == ITEM_MAXUP:
                            if self.my_char.bomb_max < 10:
                                self.my_char.bomb_max += 1
                            self.map[y][x] = ROAD
                            pyxel.play(3,pyxel.sounds[8])
                        elif obj == ITEM_LENUP:
                            if self.my_char.bomb_len < 5:
                                self.my_char.bomb_len += 1
                            self.map[y][x] = ROAD
                            pyxel.play(3,pyxel.sounds[8])
            ### スペースキーの判定　：爆弾設置
            if pyxel.btn(pyxel.KEY_SPACE):
                if self.map[self.my_char.y//16][self.my_char.x//16] != BOMB and self.map[self.my_char.y//16][self.my_char.x//16] != O_GATE:
                    if len(self.bombs) < self.my_char.bomb_max:
                        bomb = Bomb(self.my_char.x, self.my_char.y)
                        self.map[int(bomb.y/16)][int(bomb.x/16)] = BOMB
                        self.bombs.append(bomb)
                        pyxel.play(0,pyxel.sounds[0])

            ### ステージクリアの判定
            if self.map[self.my_char.y//16][self.my_char.x//16] == O_GATE:
                if len(self.tekis) == 0 or pyxel.btn(pyxel.KEY_0):
                    self.stage_num += 1
                    self.init_stage()
                    return
            ### 自キャラと敵キャラの当たり判定
            for teki in self.tekis:
                if round(teki.x/16)==self.my_char.x//16 and round(teki.y/16)==self.my_char.y//16:
                    self.gameover_flag = True
                    pyxel.play(1,pyxel.sounds[5])
                    self.gameover_counter = 120
                    return


        ### 各オブジェクトの更新処理
        self.my_char.update(self.map) # 自キャラ更新
        for teki in self.tekis:       # 敵キャラ更新
            teki.update(self.map)
        for bomb in self.bombs:       # 爆弾の更新
            bomb.update()
            if bomb.count < -12:
                self.bakuha_check(True,int(bomb.x/16),int(bomb.y/16))
                self.map[int(bomb.y/16)][int(bomb.x/16)] = ROAD
                self.bombs.remove(bomb)
            elif bomb.count < 0:
                self.bakuha_check(False,int(bomb.x/16),int(bomb.y/16))
                pyxel.play(1,pyxel.sounds[2])
        for mes in self.messages:     # メッセージの更新
            mes.update()

    def bakuha_check(self, hakai_flag, x, y):
        for i in range(4):
            wx = x + D[i][0]
            wy = y + D[i][1]
            count = 0
            self.stop_flag = False
            while wx > 0 and wx < 16 and wy > 0 and wy < 12 and count < self.my_char.bomb_len and self.stop_flag == False:
                self.bakuha(hakai_flag, wx, wy)
                wx = wx + D[i][0]
                wy = wy + D[i][1]
                count += 1
                #print("{} {} {}".format(i,self.my_char.bomb_len,count))

    def bakuha(self, hakai_flag, bx, by):
        if self.map[by][bx] == ROAD:
            self.map[by][bx] = EXPLO
        elif self.map[by][bx] == BOMB:
            for bomb in self.bombs:
                if bomb.x // 16 == bx and bomb.y // 16 == by:
                    if bomb.count > 0:
                        bomb.count = 0
        elif self.map[by][bx] == C_GATE:
            self.stop_flag = True
            if hakai_flag:
                self.map[by][bx] = O_GATE
            self.stop_flag = True
        elif self.map[by][bx] == WALL:
            self.stop_flag = True
        elif self.map[by][bx] == BLOCK or self.map[by][bx] == BROKENBLK:
            self.stop_flag = True
            self.map[by][bx] = BROKENBLK
            if hakai_flag:
                self.map[by][bx] = ROAD
                r = pyxel.rndi(0,40)
                if r == 0:
                    self.map[by][bx] = ITEM_MAXUP
                    pyxel.play(2,pyxel.sounds[1])
                elif r == 1:
                    self.map[by][bx] = ITEM_LENUP
                    pyxel.play(2,pyxel.sounds[1])
        for teki in self.tekis:
            if round(teki.x / 16) == bx and round(teki.y / 16) == by:
                if isinstance(teki,Teki1):
                    self.messages.append(Message(teki.x,teki.y,"100"))
                    self.score += 100
                elif isinstance(teki,Teki2):
                    self.messages.append(Message(teki.x,teki.y,"300"))
                    self.score += 300
                self.tekis.remove(teki)
                if len(self.tekis) == 0:
                    pyxel.play(0,pyxel.sounds[4])
        if round(self.my_char.x / 16) == bx and round(self.my_char.y / 16) == by:
            self.gameover_flag = True
            pyxel.play(0,pyxel.sounds[5])
            self.gameover_counter = 120
            return

    def draw(self):
        ### タイトル画面表示状態の時の描画処理
        if self.showtitle_flag:
            pyxel.cls(0)
            pyxel.blt(10,0,2,0,0,256,238)
            #pyxel.text(100,220,"Push EnterKey to Start!",pyxel.frame_count%15+1)
            if self.showtitle_counter > 0 and (pyxel.frame_count//2)%3 == 0:
                #pyxel.blt(0,180,1,0,0,256,30)
                pyxel.rect(0,180,256,30,0)
            return
        ### ゲームクリア後の描画処理
        if self.gameclear_flag == True:
            pyxel.cls(6)
            pyxel.blt(10,0,1,0,0,256,238)
            #pyxel.text(80,90,"GAME CLEAR!",7)
            return
        ### ステージ更新処理中の描画処理
        if self.stageclear_flag == True:
            pyxel.cls(0)
            pyxel.text(120,100,"STAGE {}".format(self.stage_num+1),7)
            return
        ### 情報の描画
        pyxel.cls(0)
        pyxel.text(20,220,"TIME {:>3}".format(self.left_time//48),7)
        pyxel.text(120,220,"{:>6}".format(self.score),7)
        pyxel.text(220,220,"STAGE {:>2}".format(self.stage_num+1),7)
        ### マップの描画
        #pyxel.bltm(0,0,0,0,0,272,208)
        for y in range(13):
            for x in range(17):
                pyxel.blt(x*16,y*16,0,self.map[y][x]*16,0,16,16)
                if self.map[y][x] == EXPLO:
                    self.map[y][x] = ROAD
        self.my_char.draw()       # 自キャラの描画 
        for teki in self.tekis:   # 敵キャラの描画
            teki.draw()
        for bomb in self.bombs:   # 爆弾の描画
            bomb.draw()
        for mes in self.messages: # メッセージの描画
            mes.draw()
            if mes.count < 0:
                self.messages.remove(mes)
        ### ゲームオーバー時の描画処理
        if self.gameover_flag == True:
            pyxel.blt(self.my_char.x,self.my_char.y,0,80,16,16,16,3)
            pyxel.text(self.my_char.x-8,self.my_char.y-8,"GAME OVER!!!",pyxel.frame_count%15+1)

    def setMap(self):
        if self.stage_num == 0:
            self.map = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,9,0,2,2,2,7,0,2,2,0,0,2,7,2,2,1],
                         [1,0,1,0,1,7,1,0,1,0,1,0,1,0,1,2,1],
                         [1,0,2,2,0,0,0,2,0,0,2,0,0,0,2,0,1],
                         [1,0,1,3,1,0,1,2,1,0,1,0,1,0,1,0,1],
                         [1,0,0,0,0,0,0,0,0,0,2,7,0,0,2,0,1],
                         [1,0,1,0,1,0,1,0,1,2,1,2,1,0,1,0,1],
                         [1,0,0,2,2,2,2,0,0,2,0,0,0,0,0,0,1],
                         [1,0,1,0,1,0,1,7,1,0,1,0,1,2,1,0,1],
                         [1,0,0,2,0,0,0,0,0,0,0,0,2,7,2,0,1],
                         [1,0,1,2,1,0,1,0,1,0,1,0,1,2,1,0,1],
                         [1,0,0,7,0,0,2,2,0,0,0,0,0,0,0,0,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        elif self.stage_num == 1:
            self.map = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,9,0,2,2,2,2,2,2,2,2,2,2,7,2,8,1],
                         [1,0,1,2,1,2,2,2,2,2,2,2,1,0,1,2,1],
                         [1,0,2,2,1,1,2,2,2,2,2,2,1,0,2,0,1],
                         [1,2,1,2,1,2,2,0,0,7,2,2,1,0,1,0,1],
                         [1,2,2,2,2,2,2,0,0,0,2,2,0,0,2,0,1],
                         [1,2,2,0,1,2,2,7,0,0,1,2,1,0,1,0,1],
                         [1,2,2,2,1,2,2,2,2,2,2,2,1,0,0,0,1],
                         [1,0,1,0,1,0,1,8,1,0,1,0,1,2,1,0,1],
                         [1,0,2,2,0,0,0,0,0,0,1,0,2,8,2,0,1],
                         [1,0,1,1,1,0,1,1,1,2,2,1,1,2,1,0,1],
                         [1,0,0,0,2,2,2,2,3,2,2,0,0,0,0,0,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        elif self.stage_num == 2:
            self.map = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,9,0,2,2,2,0,0,2,2,0,0,2,0,2,2,1],
                         [1,0,2,2,2,7,1,0,2,0,1,3,1,0,1,2,1],
                         [1,0,2,2,1,1,1,1,0,2,2,2,0,0,2,0,1],
                         [1,0,2,2,1,0,1,2,2,2,1,0,1,0,1,7,1],
                         [1,0,2,2,2,2,2,2,2,2,2,8,2,2,2,0,1],
                         [1,0,2,0,2,1,1,1,1,1,1,2,1,2,1,2,1],
                         [1,0,0,2,2,2,2,0,0,2,0,0,0,0,0,0,1],
                         [1,0,1,0,1,0,1,8,1,0,1,0,1,2,1,0,1],
                         [1,0,0,2,0,7,0,0,0,0,0,0,2,8,2,0,1],
                         [1,0,1,2,1,0,1,0,1,0,1,0,1,2,1,0,1],
                         [1,0,0,2,2,0,2,2,0,0,0,0,0,0,0,0,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]



App()

