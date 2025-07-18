#pylint:disable=W0212
#pylint:disable=W0125
#pylint:disable=W0702
#pylint:disable=W0201
#pylint:disable=W0613
import pygame, data, numpy as np

all_level_num=9
font_manager = {}

class Calc:#计算类，用于处理特殊的计算

    def __init__(self):
        pass

    def create_pos(self,a, b, c, d):
        # 生成包围框里所有可能的坐标
        arr = np.mgrid[a:b, c:d].reshape(2, -1).T
        return arr

    def calc(self,a, b, c, d, t):
        return a * (1 - t) ** 3 + b * 3 * t * (1 - t) ** 2 + c * 3 * t ** 2 * (1 - t) + d * t ** 3

    def transform(self,pic, size):  # 部分版本pygame的transform不支持浮点，之前写过的懒得改了
        return pygame.transform.scale(pic, (int(size[0]), int(size[1])))

    def transform1(self,pic, size):  # 部分版本pygame的transform不支持浮点，之前写过的懒得改了
        return pygame.transform.smoothscale(pic, (int(size[0]), int(size[1])))

    def cubic_bezier(self,abcd, x):
        [x1, y1, x2, y2] = abcd
        if x1 == y1 and x2 == y2:
            return x
        epsilon = 0.0001
        start, end = 0, 1
        P0, P1, P2, P3 = 0, x1, x2, 100
        while True:
            mid = (start + end) / 2
            point_on_curve = (1 - mid) ** 3 * P0 + 3 * mid * (1 - mid) ** 2 * P1 + \
                             3 * mid ** 2 * (1 - mid) * P2 + mid ** 3 * P3
            if abs(point_on_curve - x) < epsilon:
                break
            elif point_on_curve > x:
                end = mid
            else:
                start = mid
        t = mid
        return round(self.calc(0, y1, y2, 100, t), 6)

    def pos(self,now_wh,old_xy,old_wh):
        return now_wh*old_xy/old_wh
Calc=Calc()

class main:  # 主程序
    def __init__(self, main_rect):  # 初始化
        self.main_rect=main_rect
        self.main_sf = pygame.Surface((self.main_rect.width, self.main_rect.height))
        self.mode = 'home'   # 'home':主界面  'choose_level':选关   'level_数字':关卡   'choose_more_level':玩家自制关卡选关  'more_level_数字':关卡
        self.can_mouse_down=1
        self.Home=Home(self.main_rect)
        self.Choose_Level=Choose_Level(self.main_rect)
        self.FadeIn_Animation=FadeIn_Animation(self.main_rect)
        self.AC_Animation=AC_Animation(self.main_rect)
        self.animation_t = 0
        self.bg_alpha = 0
        self.AI = 0
        self.AI_way = None
    def modify_rect(self, main_rect):  # 修改参数
        self.main_rect=main_rect
        self.main_sf = pygame.Surface((self.main_rect.width, self.main_rect.height))
        self.Home.modify_rect(main_rect)
        self.Choose_Level.modify_rect(main_rect)
        self.FadeIn_Animation.modify_rect(main_rect)
        self.AC_Animation.modify_rect(main_rect)
        try:
            self.Level.modify_rect(main_rect)
        except:
            pass
    def update(self, events):  # 监测按键并执行
        # for event in events:
        #    pass
        self.draw_to_sf()
    def draw_to_sf(self):
        if self.mode == 'home':
            self.Home.draw(self.main_sf)
            if self.Home.button_level_pos[1] >= 1.02:
                self.mode='choose_level'
                self.can_mouse_down=1
            if self.can_mouse_down and pygame.mouse.get_pressed(3)[0] and (
                    pygame.Rect(self.main_rect.width*self.Home.button_level_pos[0] + self.main_rect.x,
                                self.main_rect.height*self.Home.button_level_pos[1] + self.main_rect.y,
                                self.main_rect.width * 250 / 1110, self.main_rect.height * 100 / 619).collidepoint(
                            pygame.mouse.get_pos())):
                self.Home.name_start, self.Home.name_end = self.Home.name_end, self.Home.name_start
                self.Home.button_more_level_start, self.Home.button_more_level_end = self.Home.button_more_level_end, self.Home.button_more_level_start
                self.Home.button_level_start, self.Home.button_level_end = self.Home.button_level_end, self.Home.button_level_start
                self.can_mouse_down=0
        elif self.mode == 'choose_level':
            self.Home.draw_bg(self.main_sf)
            self.Choose_Level.draw(self.main_sf)
            if self.can_mouse_down==0:
                if self.bg_alpha>=255:
                    self.mode='level'
                    self.can_mouse_down=1
                self.FadeIn_Animation.draw(self.main_sf,self.bg_alpha)
                self.bg_alpha+=25
            for i,pos in enumerate(self.Choose_Level.choose_button):
                if self.can_mouse_down and pygame.mouse.get_pressed(3)[0] and pos.collidepoint(pygame.mouse.get_pos()):
                    self.Level=Level(i+1,self.main_rect)
                    self.AI = 0
                    self.can_mouse_down=0
                    self.bg_alpha = 0
            if self.can_mouse_down and pygame.mouse.get_pressed(3)[0] and pygame.Rect(self.Choose_Level.cancel_rect.x+self.main_rect.x,
                           self.Choose_Level.cancel_rect.y+self.main_rect.y,
                           self.Choose_Level.cancel_rect.width,
                           self.Choose_Level.cancel_rect.height).collidepoint(pygame.mouse.get_pos()):
                self.mode='home'
                self.Home.button_more_level_pos[1]=self.Home.button_more_level_end[1]
                self.Home.button_level_pos[1] = self.Home.button_level_end[1]
                self.Home.name_pos[1] = self.Home.name_end[1]
                self.Home.name_start, self.Home.name_end = self.Home.name_end, self.Home.name_start
                self.Home.button_more_level_start, self.Home.button_more_level_end = self.Home.button_more_level_end, self.Home.button_more_level_start
                self.Home.button_level_start, self.Home.button_level_end = self.Home.button_level_end, self.Home.button_level_start

        elif self.mode=='level':
            self.main_sf.fill((29, 83, 0xbb))
            self.Level.draw_tools(self.main_sf)
            self.Level.draw_ans(self.main_sf)
            self.Level.draw_board_bg(self.main_sf)
            self.Level.draw_ans_board(self.main_sf) 
            self.Level.draw_board(self.main_sf,self.can_mouse_down) 
            if self.can_mouse_down==0 and self.AI==0:
                if self.animation_t>=100:
                    self.animation_t = 0
                    self.can_mouse_down = 1
                    if self.Level.level+1 > all_level_num:
                        self.mode='choose_level'
                        return
                    self.Level = Level(self.Level.level + 1, self.main_rect)
                    return
                self.AC_Animation.draw(self.main_sf,self.animation_t)
                self.animation_t+=10
            if self.Level.board.is_win(np.array(self.Level.target)) and self.can_mouse_down:
                self.can_mouse_down = 0
                self.animation_t=0
            if self.AI:
                try:
                    self.Level.board.draw_color(self.AI_way[1][self.AI-1])
                    self.AI += 1
                except:
                    self.AI = 0

            if self.can_mouse_down and pygame.mouse.get_pressed(3)[0] and \
                    self.Level.again_rect.x>=0 and self.Level.home_rect.x>=0 and self.Level.next_rect.x>=0:
                if pygame.Rect(self.Level.again_rect.x+self.main_rect.x,
                               self.Level.again_rect.y+self.main_rect.y,
                               self.Level.again_rect.width,
                               self.Level.again_rect.height).collidepoint(pygame.mouse.get_pos()):
                    self.Level = Level(self.Level.level, self.main_rect)
                    self.AI=0
                elif pygame.Rect(self.Level.next_rect.x+self.main_rect.x,
                               self.Level.next_rect.y+self.main_rect.y,
                               self.Level.next_rect.width,
                               self.Level.next_rect.height).collidepoint(pygame.mouse.get_pos()):
                    self.can_mouse_down=0
                    self.animation_t = 0
                elif pygame.Rect(self.Level.home_rect.x+self.main_rect.x,
                               self.Level.home_rect.y+self.main_rect.y,
                               self.Level.home_rect.width,
                               self.Level.home_rect.height).collidepoint(pygame.mouse.get_pos()):
                    self.mode = 'choose_level'
                elif pygame.mouse.get_pressed(3)[0] and pygame.Rect(self.Level.AI_button.x+self.main_rect.x,
                                                                    self.Level.AI_button.y+self.main_rect.y,
                                                                    self.Level.AI_button.width,
                                                                    self.Level.AI_button.height).collidepoint(pygame.mouse.get_pos()):
                    self.AI = 1
                    self.AI_way=self.Level.board.AI_Answer(self.Level.target)
                    self.can_mouse_down=0

    def draw_to_screen(self, screen):  # 绘制到屏幕
        screen.blit(self.main_sf, (self.main_rect.x, self.main_rect.y))

class Home:
    def __init__(self,main_rect):
        self.main_rect=main_rect

        self._image_bg = pygame.image.load('image/bg/bg.png').convert_alpha()
        self._image_bg1 = pygame.image.load('image/bg/bg1.png').convert_alpha()
        self._button = pygame.image.load('image/button/button.png')
        self.image_bg = Calc.transform(self._image_bg, (main_rect.width, main_rect.height)).convert_alpha()
        self.image_bg1 = Calc.transform(self._image_bg1,
                                        (Calc.pos(self._image_bg1.get_width(),main_rect.height,self._image_bg1.get_height()),
                                         main_rect.height)).convert_alpha()
        self.image_button = Calc.transform(self._button,
                                          (self.main_rect.width * 250 / 1110, self.main_rect.height * 100 / 619)).convert_alpha()

        self.name_start = (100 / 1110, 639 / 619)
        self.name_end = (100 / 1110, 80 / 619)
        self.name_pos = [100 / 1110, 639 / 619]
        self.button_level_start = (600 / 1110, 639 / 619)
        self.button_level_end = (600 / 1110, 300 / 619)
        self.button_level_pos = [600 / 1110, 639 / 619]
        self.button_more_level_start = (600 / 1110, 639 / 619)
        self.button_more_level_end = (600 / 1110, 450 / 619)
        self.button_more_level_pos = [600 / 1110, 639 / 619]

    def modify_rect(self,main_rect):
        self.main_rect=main_rect
        self.image_bg = Calc.transform(self._image_bg, (main_rect.width, main_rect.height))
        self.image_bg1 = Calc.transform(self._image_bg1,
                                        (Calc.pos(self._image_bg1.get_width(), main_rect.height,
                                                  self._image_bg1.get_height()),
                                         main_rect.height))
        self.image_button = Calc.transform(self._button,
                                           (self.main_rect.width * 250 / 1110, self.main_rect.height * 100 / 619))

    def show_text(self, screen, text, color=(0, 0), pos=(0, 0), size=30):
        size = int(size)
        if size in font_manager:
            font = font_manager[size]
        else:
            font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
        screen.blit(font.render((text), True, color), pos)

    def draw_bg(self,screen):
        screen.blit(self.image_bg, (0, 0))
        screen.blit(self.image_bg1, (self.main_rect.width / 2 - self.image_bg1.get_width() / 2,
                                     Calc.pos(self.main_rect.height, 20, 619)))
        screen.blit(self.image_button, (self.main_rect.width * self.button_level_pos[0],
                                        self.main_rect.height * self.button_level_pos[1]))
        screen.blit(self.image_button, (self.main_rect.width * self.button_more_level_pos[0],
                                        self.main_rect.height * self.button_more_level_pos[1]))

    def draw(self,screen):
        self.name_pos[1] += (self.name_end[1] - self.name_pos[1]) / 3
        self.button_level_pos[1] += (self.button_level_end[1] - self.button_level_pos[1]) / 3
        self.button_more_level_pos[1] += (self.button_more_level_end[1] - self.button_more_level_pos[1]) / 3

        self.draw_bg(screen)
        self.show_text(screen,'横涂纵刷', (255, 255, 255), (self.main_rect.width*self.name_pos[0],
                                                    self.main_rect.height*self.name_pos[1]),
                       Calc.pos(self.main_rect.height,160,619))
        self.show_text(screen,'开始游戏', (127, 127, 127), (
            self.main_rect.width * self.button_level_pos[0] + (Calc.pos(self.main_rect.width,250,1110) / 2 - Calc.pos(self.main_rect.height,40,619) * 2),
            self.main_rect.height * self.button_level_pos[1] + (Calc.pos(self.main_rect.height,100,619) / 2 - Calc.pos(self.main_rect.height,40,619) / 2)),
                       Calc.pos(self.main_rect.height,40,619))
        self.show_text(screen,'玩家自制关', (127, 127, 127), (
            self.main_rect.width * self.button_more_level_pos[0] + (Calc.pos(self.main_rect.width,250,1110) / 2 - Calc.pos(self.main_rect.height,40,619) * 2.5),
            self.main_rect.height * self.button_more_level_pos[1] + (Calc.pos(self.main_rect.height,100,619) / 2 - Calc.pos(self.main_rect.height,40,619) / 2)),
                       Calc.pos(self.main_rect.height,40,619))

class Choose_Level:

    def __init__(self,main_rect):
        self.main_rect = main_rect
        self._button = pygame.image.load('image/button/level_button.png').convert_alpha()
        self._cancel = pygame.image.load('image/button/返回.png').convert_alpha()
        self.image_level_button = Calc.transform(self._button,
                                            (self.main_rect.width * 150 / 1110, self.main_rect.height * 150 / 619)).convert_alpha()
        self.image_cancel = Calc.transform(self._cancel,
                                      (self.main_rect.width * 75 / 1110, self.main_rect.height * 75 / 619)).convert_alpha()

    def modify_rect(self,main_rect):
        self.main_rect=main_rect
        self.image_level_button = Calc.transform(self._button,
                                            (self.main_rect.width * 150 / 1110, self.main_rect.height * 150 / 619))
        self.image_cancel = Calc.transform(self._cancel,
                                      (self.main_rect.width * 75 / 1110, self.main_rect.height * 75 / 619))

    def show_text(self, screen, text, color=(0, 0), pos=(0, 0), size=30):
        size = int(size)
        if size in font_manager:
            font = font_manager[size]
        else:
            font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
        screen.blit(font.render((text), True, color), pos)
        
    def show_text_center(self, screen, text, color=(0, 0), ct=(0, 0), size=30):
        size = int(size)
        if size in font_manager:
            font = font_manager[size]
        else:
            font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
        word=font.render((text), True, color)
        screen.blit(word, (ct[0]-word.get_width()/2,ct[1]-word.get_height()/2))

    def draw(self,screen):
        self.choose_button=[]
        for i in range(1, 6):
            x, y = (self.main_rect.width * 50 / 1110) + (i - 1) * (self.main_rect.width * 200 / 1110), \
                   self.main_rect.height * 20 / 619
            screen.blit(self.image_level_button, (x, y))
            self.show_text_center(screen,str(i), (127, 127, 127), (
                x + self.main_rect.width * 150 / 1110 / 2,
                y + self.main_rect.height * 150 / 619 / 2),
                self.main_rect.height * 80 / 619)
            self.choose_button.append(pygame.Rect(x+self.main_rect.x,
                                                   y+self.main_rect.y,
                                                   self.main_rect.width * 150 / 1110,
                                                   self.main_rect.height * 150 / 619))
        for i in range(6,all_level_num+1):
            x, y = (self.main_rect.width * 50 / 1110) + (i - 5 - 1) * (self.main_rect.width * 200 / 1110), \
                   self.main_rect.height * 200 / 619
            screen.blit(self.image_level_button, (x, y))
            self.show_text_center(screen, str(i), (127, 127, 127), (
                x + self.main_rect.width * 150 / 1110 / 2,
                y + self.main_rect.height * 150 / 619 / 2),
                                  self.main_rect.height * 80 / 619)
            self.choose_button.append(pygame.Rect(x + self.main_rect.x,
                                                  y + self.main_rect.y,
                                                  self.main_rect.width * 150 / 1110,
                                                  self.main_rect.height * 150 / 619))
        self.cancel_rect=pygame.Rect(self.main_rect.width * 1000 / 1110,
                                     self.main_rect.height * 500 / 619,
                                     self.main_rect.width * 75 / 1110,
                                     self.main_rect.height * 75 / 619)
        screen.blit(self.image_cancel, (self.cancel_rect.x,self.cancel_rect.y))

class Level:
    def __init__(self,level,main_rect):
        self.level=level
        self.main_rect=main_rect
        self._home = pygame.image.load('image/button/home.png').convert_alpha()
        self._next = pygame.image.load('image/button/next.png').convert_alpha()
        self._again = pygame.image.load('image/button/again.png').convert_alpha()
        self.image_home = Calc.transform(self._home,
                                    (Calc.pos(self.main_rect.width,75,1200), Calc.pos(self.main_rect.height,75,674)))
        self.image_next = Calc.transform(self._next,
                                    (Calc.pos(self.main_rect.width,75,1200), Calc.pos(self.main_rect.height,75,674)))
        self.image_again = Calc.transform(self._again,
                                     (Calc.pos(self.main_rect.width,75,1200), Calc.pos(self.main_rect.height,75,674)))
        self.brush=self.brush = pygame.image.load('image/button/刷子.png').convert_alpha()

        self.target = data.level[level]['target']
        self.paint_lie = data.level[level]['paint_lie']
        self.paint_hang = data.level[level]['paint_hang']
        self.board = Board(len(self.target), len(self.target[0]), self.paint_lie, self.paint_hang,
                           np.array([63, 187, 208]))
        self.target_board = Board(len(self.target), len(self.target[0]), self.paint_lie, self.paint_hang)
        self.target_board.board = np.array(self.target)
        self.target_board.draw()
        self.home_rect=pygame.Rect(-1,-1,-1,-1)
        self.next_rect=pygame.Rect(-1,-1,-1,-1)
        self.again_rect=pygame.Rect(-1,-1,-1,-1)

    def modify_rect(self,main_rect):
        self.main_rect=main_rect
        self.image_home = Calc.transform(self._home,
                                         (Calc.pos(self.main_rect.width, 75, 1200), Calc.pos(self.main_rect.height, 75, 674)))
        self.image_next = Calc.transform(self._next,
                                         (Calc.pos(self.main_rect.width, 75, 1200), Calc.pos(self.main_rect.height, 75, 674)))
        self.image_again = Calc.transform(self._again,
                                          (Calc.pos(self.main_rect.width, 75, 1200), Calc.pos(self.main_rect.height, 75, 674)))

    def show_text(self, screen, text, color=(0, 0), pos=(0, 0), size=30):
        size = int(size)
        if size in font_manager:
            font = font_manager[size]
        else:
            font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
        screen.blit(font.render((text), True, color), pos)
        
    def show_text_center(self, screen, text, color=(0, 0), ct=(0, 0), size=30):
        size = int(size)
        if size in font_manager:
            font = font_manager[size]
        else:
            font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
        word=font.render((text), True, color)
        screen.blit(word, (ct[0]-word.get_width()/2,ct[1]-word.get_height()/2))

    def draw_tools(self,screen):#绘制工具栏
        offset_x, offset_y = Calc.pos(self.main_rect.width,6,1110), Calc.pos(self.main_rect.height , 6 , 619)
        self.tool_rect=pygame.Rect(Calc.pos(self.main_rect.width , 700 , 1200),
                                   Calc.pos(self.main_rect.height,560,674),
                                   Calc.pos(self.main_rect.width,420,1200),
                                   Calc.pos(self.main_rect.height,95,674))
        pygame.draw.rect(screen, (117, 119, 162), pygame.Rect(self.tool_rect.x + offset_x,
                                                                    self.tool_rect.y + offset_y,
                                                                    self.tool_rect.width,
                                                                    self.tool_rect.height), border_radius=30)
        pygame.draw.rect(screen, (252, 175, 123), self.tool_rect, border_radius=30)

        self.again_rect = pygame.Rect(Calc.pos(self.main_rect.width,750,1200),
                                 Calc.pos(self.main_rect.height,570,674),
                                 Calc.pos(self.main_rect.width,75,1200),
                                 Calc.pos(self.main_rect.height,75,674))
        self.next_rect = pygame.Rect(Calc.pos(self.main_rect.width,870,1200),
                                Calc.pos(self.main_rect.height,570,674),
                                Calc.pos(self.main_rect.width,75,1200),
                                Calc.pos(self.main_rect.height,75,674))
        self.home_rect = pygame.Rect(Calc.pos(self.main_rect.width,990,1200),
                                Calc.pos(self.main_rect.height,570,674),
                                Calc.pos(self.main_rect.width,75,1200),
                                Calc.pos(self.main_rect.height,75,674))
        screen.blit(self.image_again, (self.again_rect.x, self.again_rect.y))
        screen.blit(self.image_next, (self.next_rect.x, self.next_rect.y))
        screen.blit(self.image_home, (self.home_rect.x, self.home_rect.y))

    def draw_ans(self,screen):#绘制目标图像背景
        offset_x, offset_y = Calc.pos(self.main_rect.width, 6, 1110), Calc.pos(self.main_rect.height, 6, 619)
        self.ans_rect = pygame.Rect(Calc.pos(self.main_rect.width,700,1200),
                                    Calc.pos(self.main_rect.height,60,674),
                                    Calc.pos(self.main_rect.width,420,1200),
                                    Calc.pos(self.main_rect.height,480,674))
        pygame.draw.rect(screen, (40, 127, 183), pygame.Rect(self.ans_rect.x + offset_x,
                                                             self.ans_rect.y + offset_y,
                                                             self.ans_rect.width,
                                                             self.ans_rect.height), border_radius=30)
        pygame.draw.rect(screen, (0x3b, 0xc4, 0xb1), self.ans_rect, border_radius=30)

    def draw_board_bg(self,screen):#绘制盘面背景
        offset_x, offset_y = Calc.pos(self.main_rect.width, 6, 1110), Calc.pos(self.main_rect.height, 6, 619)
        self.board_bg_rect = pygame.Rect(Calc.pos(self.main_rect.width,50,1200),
                                         Calc.pos(self.main_rect.height,50,674),
                                         Calc.pos(self.main_rect.width,600,1200),
                                         Calc.pos(self.main_rect.height,600,674))
        pygame.draw.rect(screen, (42, 124, 196), pygame.Rect(self.board_bg_rect.x + offset_x,
                                                             self.board_bg_rect.y + offset_y,
                                                             self.board_bg_rect.width,
                                                             self.board_bg_rect.height), border_radius=30)
        pygame.draw.rect(screen, (63, 187, 208), self.board_bg_rect, border_radius=30)
        self.show_text(screen, "第" + str(self.level) + '关', (255, 255, 255),
                       (self.main_rect.width * 60 / 1200, self.main_rect.height * 60 / 674),
                       self.main_rect.height * 40 / 619)

    def draw_ans_board(self,screen):
        self.show_text(screen, "目标图像:", (255, 255, 255), (Calc.pos(self.main_rect.width,710,1200),
                                                          Calc.pos(self.main_rect.height,70,674)),
                       Calc.pos(self.main_rect.height,40,619))

        tg_x, tg_y = (Calc.pos(self.main_rect.width,700,1200) +
                      (Calc.pos(self.main_rect.width,420,1200) / 2 -
                       Calc.pos(self.main_rect.width,250,990) / 2),
                      Calc.pos(self.main_rect.height,60,674) +
                      (Calc.pos(self.main_rect.height,480,674) / 2 -
                       Calc.pos(self.main_rect.height,250,557) / 2))
        screen.blit(Calc.transform1(self.target_board._sf,
                                    (Calc.pos(self.main_rect.width,250,990),
                                     Calc.pos(self.main_rect.height,250,557))), (tg_x, tg_y))
        self.AI_button=pygame.Rect(tg_x, tg_y + Calc.pos(self.main_rect.height,265,557),
                                     Calc.pos(self.main_rect.width,250,990),
                                     Calc.pos(self.main_rect.height,45,557))
        pygame.draw.rect(screen, (0, 0, 0), self.AI_button)
        self.show_text_center(screen,"AI过关",(255,255,255),(self.AI_button.x + self.AI_button.width/2 , self.AI_button.y + self.AI_button.height/2),self.main_rect.height*30/557)

    def draw_board(self,screen,can_mouse_down):
        self.board.draw() 
        xxx = 350
        board_width, board_height = self.main_rect.width * xxx / 990, self.main_rect.height * xxx / 557
        board_rect = pygame.Rect(self.board_bg_rect.x + (self.board_bg_rect.width / 2 - board_width / 2),
                                 self.board_bg_rect.y + (self.board_bg_rect.height / 2 - board_height / 2),
                                 board_width, board_height)
        one_gezi = pygame.Rect(0, 0, board_width / len(self.target), board_height / len(self.target[0]))
        brush_rect = pygame.Rect(0, 0, one_gezi.width / 2, one_gezi.height / 2)
        self.board_rect=board_rect
        screen.blit(
            Calc.transform1(self.board._sf, (board_rect.width, board_rect.height)),
            (board_rect.x, board_rect.y))
        brush = Calc.transform(self.brush, (brush_rect.width, brush_rect.height))
        if '竖着的刷子':
            br_x = self.board_bg_rect.x + ((board_rect.x - self.board_bg_rect.x) / 2 - brush_rect.width / 2)
            br_yyy = np.arange(0, board_rect.height + 1, board_rect.height / len(self.target)).astype(np.int32)
            for i in range(1, len(self.target) + 1):
                if '给刷子上色':
                    brush1 = brush.copy()
                    bh_np = pygame.surfarray.pixels3d(brush1)
                    bh_np[np.all(bh_np == [0x99, 0x66, 0xff], axis=-1)] = self.paint_hang[i - 1][0]
                    del bh_np
                br_y = board_rect.y+br_yyy[i-1]+(one_gezi.height / 2 - brush_rect.height / 2)
                screen.blit(brush1, (br_x, br_y))
                if can_mouse_down and pygame.mouse.get_pressed(3)[0] and \
                        pygame.Rect(self.board_bg_rect.x + self.main_rect.x, board_rect.y+br_yyy[i-1] + self.main_rect.y, board_rect.x-self.board_bg_rect.x, one_gezi.height) \
                                .collidepoint(pygame.mouse.get_pos()):
                    self.board.draw_color(i)
        if "横着的刷子":
            br_y = self.board_bg_rect.y + ((board_rect.y - self.board_bg_rect.y) / 2 - brush_rect.height / 2)
            br_xxx=np.arange(0,board_rect.width+1,board_rect.width/len(self.target[0])).astype(np.int32)
            for i in range(len(self.target) + 1, len(self.target) + len(self.target[0]) + 1):
                if '给刷子上色':
                    brush1 = brush.copy()
                    bh_np = pygame.surfarray.pixels3d(brush1)
                    bh_np[np.all(bh_np == [0x99, 0x66, 0xff], axis=-1)] = self.paint_lie[0][i - len(self.target) - 1]
                    del bh_np
                br_x = board_rect.x + br_xxx[i - 1 - len(self.target)]+(one_gezi.width / 2 - brush_rect.width / 2)
                screen.blit(brush1, (br_x, br_y))
                if can_mouse_down and pygame.mouse.get_pressed(3)[0] and \
                        pygame.Rect(board_rect.x+br_xxx[i - 1 - len(self.target)] + self.main_rect.x, self.board_bg_rect.y + self.main_rect.y, one_gezi.width,board_rect.y-self.board_bg_rect.y) \
                                .collidepoint(pygame.mouse.get_pos()):
                    self.board.draw_color(i)
        if self.level>=7:
            self.draw_ste(screen)
    def draw_ste(self,screen):
        self.show_text_center(screen,"此关为复合关，每行每列刷子的颜色不再单一",
                              (255,255,255),(self.board_rect.x+self.board_rect.width/2,self.board_rect.y+self.board_rect.height*1.1),self.board_rect.width/15)
class AC_Animation:#AC动画
    def __init__(self,main_rect):
        self.main_rect=main_rect
        self.image_AC = pygame.image.load('image/other/congratulation.png').convert_alpha()
        self.max_w,self.max_h=-1,-1
    def modify_rect(self,main_rect):
        self.main_rect=main_rect

    def draw(self,screen,t):
        if t<=50:
            s,e=(400/1110 , 325/619),(600/1110 , 487/619)
            bz=Calc.cubic_bezier([42, 87, 100, 128], t*2)
            w=s[0] + (e[0] - s[0]) * bz / 100
            h=s[1] + (e[1] - s[1]) * bz / 100
            self.max_w=max(self.max_w,w)
            self.max_h=max(self.max_h,h)
            screen.blit(Calc.transform(self.image_AC, (self.main_rect.width*w, self.main_rect.height*h)),
                              (self.main_rect.width / 2 - self.main_rect.width*w / 2,
                               self.main_rect.height / 2 - self.main_rect.height*h / 2))
        else:
            s,e=(self.max_w,self.max_h),(400/1110 , 325/619)
            bz=Calc.cubic_bezier([42, 0, 100, 100], (t-50)*2)
            w=s[0] + (e[0] - s[0]) * bz / 100
            h=s[1] + (e[1] - s[1]) * bz / 100
            screen.blit(Calc.transform(self.image_AC, (self.main_rect.width * w, self.main_rect.height * h)),
                        (self.main_rect.width / 2 - self.main_rect.width * w / 2,
                         self.main_rect.height / 2 - self.main_rect.height * h / 2))

class FadeIn_Animation:#渐显动画
    def __init__(self,main_rect):
        self.main_rect=main_rect
        self._sf = pygame.Surface((self.main_rect.width, self.main_rect.height), pygame.SRCALPHA).convert_alpha()
        self._sf.fill((29, 83, 0xbb))

    def modify_rect(self,main_rect):
        self.main_rect=main_rect
        self._sf = pygame.Surface((self.main_rect.width, self.main_rect.height), pygame.SRCALPHA).convert_alpha()
        self._sf.fill((29, 83, 0xbb))

    def draw(self,screen,t):
        self._sf.set_alpha(t)
        screen.blit(self._sf, (0, 0))

class Board:
    def __init__(self, width, height, paint_lie, paint_hang, bg=None):
        self.width = width
        self.height = height
        self._sf = pygame.Surface((351, 351)).convert()
        sf = pygame.surfarray.pixels3d(self._sf)
        sf[:, :] = bg if bg is not None else np.array([0x3b, 0xc4, 0xb1])
        sf[np.arange(0,351,350 / self.width).astype(np.int32), :] = [0x52, 0x71, 0xff]  # 设置x轴上的条纹
        sf[:, np.arange(0,351,350 / self.height).astype(np.int32)] = [0x52, 0x71, 0xff]  # 设置y轴上的条纹
        self.paint_lie = np.array(paint_lie)
        self.paint_hang = np.array(paint_hang)
        self.board = np.full((height, width, 3), -1)
        
        self.pos = [[None for _ in range(self.width)] for _ in range(self.height)]
        xx = np.arange(0,351,350 / self.width).astype(np.int32)
        yy = np.arange(0,351,350 / self.height).astype(np.int32)
        for i in range(self.height):
            for j in range(self.width):
                m=Calc.create_pos(xx[i],xx[i+1],yy[j],yy[j+1])
                self.pos[i][j] = m[:, 1], m[:, 0]

    def draw_color(self, num):
        if num <= self.height:
            self.board[num - 1] = self.paint_hang[num - 1]
        else:
            self.board[:, int(num - self.height - 1),:] = self.paint_lie[:, int(num - self.height - 1),:]

    def draw(self):
        sf = pygame.surfarray.pixels3d(self._sf)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j][0] != -1:
                    pos=self.pos[i][j] 
                    sf[pos]=self.board[i][j]

    def is_win(self, target):
        return np.array_equal(target, self.board)

    def AI_Answer(self,target):
        maxn=self.width+self.height+5
        n=self.width+self.height
        h = [[] for _ in range(maxn)]  # 存储每个点的出边的终点
        du = [0 for _ in range(maxn)]  # 存储每个点的入度
        def addEdge(u, v):
            h[u].append(v)
            du[v] += 1
        q = []
        def toposort():
            head = 0
            for i in range(1, n + 1):  # 寻找入度为0的点
                if du[i] == 0:  # 入度是0
                    q.append(i)  # 加入答案列表
            while head < len(q):
                u = q[head]  # 当前遍历到的入度为0的点
                head += 1
                for i in h[u]:  # 遍历当前点的出边
                    du[i] -= 1  # 当前边的终点的点的入度-1
                    if du[i] == 0:  # 如果当前边的终点的点的入度变成0
                        q.append(i)  # 加入答案列表
            if len(q) != n:  # 答案不够，图有环
                return -1
            else:
                return 1

        for i in range(1, len(target) + 1):
            for j in range(len(target) + 1, len(target[0]) + len(target) + 1):
                x, y = i - 1, j - 1 - len(target)
                if np.array_equal(self.paint_hang[x][y],self.paint_lie[x][y]):
                    continue
                if np.array_equal(target[x][y],self.paint_hang[x][y]):
                    addEdge(j, i)
                else:
                    addEdge(i, j)
        toposort()
        return len(q)-1,q[1:] #第一次刷一定会被完全覆盖，可以直接删去
