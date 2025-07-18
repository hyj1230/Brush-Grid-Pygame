import pygame,sys,paint_game
pygame.init()
WIDTH,HEIGHT=1200,650
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Brush Grid（横涂纵刷）")
font_manager = {}
def show_text(text,color=(0,0),pos=(0,0),size=30):
    size = int(size)
    if size in font_manager:
        font = font_manager[size]
    else:
        font = font_manager[size] = pygame.font.Font('方正达利体.ttf', size)
    screen.blit(font.render((text), True, color), pos)
class Window:#一个窗口类
    def __init__(self):
        self.game = paint_game.main(pygame.Rect(105,65,990,557))#游戏界面
        self.window_rect = pygame.Rect(90,15,1020,622)#窗口rect
        self.mode = 'None'
        '''
        'None':无
        'dragging':拖拽
        'resize_dragging':修改窗口宽度和高度(右下)
        '''
        
        self.offset_x = 0
        self.offset_y = 0
        self.clock = pygame.time.Clock()
    def draw(self, surface):
        fps = str(round(self.clock.get_fps()))
        mouse_pos = pygame.mouse.get_pos()
        resize_dragging_rect = pygame.Rect(self.window_rect.right-20, self.window_rect.bottom-20, 20, 20)
        if resize_dragging_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # 绘制图片
        pygame.draw.rect(surface,(235,235,235),pygame.Rect(self.window_rect.x-5,self.window_rect.y-5,self.window_rect.width+10,self.window_rect.height+10),border_radius=25)
        pygame.draw.rect(surface,(255,255,255),self.window_rect,border_radius=20)
        show_text("逆天团队-横涂纵刷, fps:" + fps,(0,0,0),(self.window_rect.x+10,self.window_rect.y+10))
        self.game.update(pygame.event.get())#游戏开始主循环
        self.game.draw_to_screen(surface)#把游戏界面绘制到窗口
    def handle_event(self, event):
        if pygame.mouse.get_pressed(3)[0]:
            if self.mode=='None':
                mouse_pos = pygame.mouse.get_pos()
                dragging_rect = pygame.Rect(self.window_rect.x,self.window_rect.y,self.window_rect.width,50)
                resize_dragging_rect = pygame.Rect(self.window_rect.right-20, self.window_rect.bottom-20, 20, 20)
                if dragging_rect.collidepoint(mouse_pos):
                    self.mode = 'dragging'
                    self.offset_x = mouse_pos[0] - self.window_rect.x
                    self.offset_y = mouse_pos[1] - self.window_rect.y
                elif resize_dragging_rect.collidepoint(mouse_pos):
                    self.mode = 'resize_dragging'
                    self.offset_x = mouse_pos[0] - (self.window_rect.right-20)
                    self.offset_y = mouse_pos[1] - (self.window_rect.bottom-20)
        else:
            self.mode='None'
        if event.type == pygame.MOUSEMOTION:
            if self.mode=='dragging':
                mouse_pos = pygame.mouse.get_pos()
                self.window_rect.x = mouse_pos[0] - self.offset_x
                self.window_rect.y = mouse_pos[1] - self.offset_y
                self.game.modify_rect(pygame.Rect(self.window_rect.x+15,self.window_rect.y+50,self.game.main_rect.width,self.game.main_rect.height))
            elif self.mode=='resize_dragging':
                mouse_pos = pygame.mouse.get_pos()
                self.window_rect.width = max(201,mouse_pos[0]-self.window_rect.x - self.offset_x + 20)
                self.window_rect.height = max(101, mouse_pos[1] - self.window_rect.y - self.offset_x + 20)
                self.game.modify_rect(pygame.Rect(self.game.main_rect.x,self.game.main_rect.y,self.window_rect.width-30,self.window_rect.height-65))

window=Window()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            window.handle_event(event)
    screen.fill((239,239,239))
    
    window.draw(screen)
    
    pygame.display.update()
    window.clock.tick(60)