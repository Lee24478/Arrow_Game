import pygame
import os 
import random
pygame.font.init()  # Initial the font , just have to do it , no reason...
pygame.mixer.init()

# Create a window to set game 
pygame.init()
WIN_RESOLUTIONS = pygame.display.Info()
# WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h  # FULLSCREEN
WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w - 700 , WIN_RESOLUTIONS.current_h - 110  #900 , 1000
WIN = pygame.display.set_mode((WIDTH , HEIGHT) , pygame.RESIZABLE)
pygame.display.set_caption("Arrow Game")  # Set game's title
ICON = pygame.image.load(os.path.join("Assets" , "game_icon.png"))
pygame.display.set_icon(ICON)  # Set game's icon

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
Turquoise = (51,230,204)  # 綠松藍色

# Load images
ARROWS_WIDTH , ARROWS_HEIGHT = 180 , 180
DOWN_DIRECTION = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "arrow.png")) , (ARROWS_WIDTH , ARROWS_HEIGHT))
LEFT_DIRECTION = pygame.transform.rotate(DOWN_DIRECTION , 270)
UP_DIRECTION = pygame.transform.rotate(DOWN_DIRECTION , 180)
RIGHT_DIRECTION = pygame.transform.rotate(DOWN_DIRECTION , 90)
MUTE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "mute.png")) , (50,50))
UNMUTE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "unmute.png")) , (50,50))
MUTE_WHITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "mute_rmbg.png")) , (50,50))
UNMUTE_WHITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "unmute_rmbg.png")) , (50,50))
ARROWS_SHOW_ON_INIT = pygame.transform.scale(pygame.image.load(os.path.join("Assets" , "direction.png")) , (80 , 80))

# Load musics
PAUSE_SOUND = pygame.mixer.Sound(os.path.join("Assets" , "don.mp3"))
PRESS_SOUND = pygame.mixer.Sound(os.path.join("Assets" , "Meow.wav"))
pygame.mixer.music.load(os.path.join("Assets" , "Meow_music.mp3"))
pygame.mixer.music.play(-1)
PAUSE_SOUND.set_volume(0.4)
PRESS_SOUND.set_volume(0.5)
pygame.mixer.music.set_volume(0.2)

# Some variables 
FPS = 60  # How fast the window updates
clock = pygame.time.Clock()
pause_state = False
on_or_off = [True , False]
F11_times = 0
sound_check = 1
unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)   

# Load record
try:
    with open(os.path.join("Assets" , "Record.txt") , 'r') as f:
        try:
            record = int(f.read())
        except:
            record = 0
except:
    record = 0

class Down(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = DOWN_DIRECTION
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0  

    def update(self , VELOCITY):
        self.rect.y += VELOCITY

class Left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = LEFT_DIRECTION
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0  

    def update(self , VELOCITY):
        self.rect.y += VELOCITY

class Up(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = UP_DIRECTION
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0  

    def update(self , VELOCITY):
        self.rect.y += VELOCITY

class Right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = RIGHT_DIRECTION
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0  

    def update(self , VELOCITY):
        self.rect.y += VELOCITY

class Arrows(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = ARROWS_SHOW_ON_INIT
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0 , WIDTH - self.rect.width)
        self.rect.y = random.randrange(0 , HEIGHT - self.rect.height)
        self.x_vel = random.randrange(-3,3)
        self.y_vel = random.randrange(-3,3)
        self.degree_list = [-3,-2,-1,1,2,3]
        self.rotate_degree = random.choice(self.degree_list)
        self.angle = 0

    def rotate(self):
        self.angle += self.rotate_degree
        self.angle %= 360
        self.image = pygame.transform.rotate(self.image_original , self.angle)
        self.image.set_colorkey(WHITE)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0
        elif self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = HEIGHT 

def update_arrows(ARROWS_LINE_NUMBER , all_sprites):
    if len(all_sprites.sprites()) == 0:
        # Add first sprite 
        down_arrow = Down()
        left_arrow = Left()
        up_arrow = Up()
        right_arrow = Right()
        ARROWS = [down_arrow , left_arrow , up_arrow , right_arrow]
        random_num = random.randrange(0,4)
        arrow = ARROWS[random_num]
        all_sprites.add(arrow)
        ARROWS_LINE_NUMBER.append(ARROWS.index(arrow))
        # Add first sprite 
    elif len(all_sprites.sprites()) < 10:
        down_arrow = Down()
        left_arrow = Left()
        up_arrow = Up()
        right_arrow = Right()
        ARROWS = [down_arrow , left_arrow , up_arrow , right_arrow]
        random_num = random.randrange(0,4)
        arrow = ARROWS[random_num]
        arrow.rect.bottom = all_sprites.sprites()[-1].rect.top - 15 
        all_sprites.add(arrow)
        ARROWS_LINE_NUMBER.append(ARROWS.index(arrow))

def draw_text(text , font , font_size , x , y , color , bold = None):
    try:
        main_font = pygame.font.Font(font , font_size)
    except:
        main_font = pygame.font.SysFont(font , font_size , bold)
    render_text = main_font.render(text , 1 , color)
    text_rect = render_text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    WIN.blit(render_text , text_rect)

def draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites):
    WIN.fill(WHITE)  # White background
    pygame.draw.rect(WIN , Turquoise , (0,0 , WIDTH/2 - ARROWS_WIDTH/2,HEIGHT))  # background of tow sides
    pygame.draw.rect(WIN , Turquoise , (WIDTH/2 + ARROWS_WIDTH/2,0 , WIDTH - (WIDTH/2 + ARROWS_WIDTH/2),HEIGHT))  # background of tow sides
    # Draw scores text #
    main_font = pygame.font.Font(os.path.join("Assets" , "ComicSansMS3.ttf") , 30)
    render_text = main_font.render(f"Arrows : {SCORE}" , 1 , BLACK)
    WIN.blit(render_text , (10,10))
    # Draw scores text #
    if record:
        # Draw record #
        main_font = pygame.font.Font(os.path.join("Assets" , "ComicSansMS3.ttf") , 30)
        render_text = main_font.render(f"Record : {record}" , 1 , BLACK)
        WIN.blit(render_text , (12,50))
        # Draw record #
    update_arrows(ARROWS_LINE_NUMBER , all_sprites)
    all_sprites.draw(WIN)
    all_sprites.update(VELOCITY)
    pygame.display.update()

def draw_init_screen():
    global WIN , WIDTH , HEIGHT , F11_times , sound_check , unmute_pos
    arrows_sprites = pygame.sprite.Group()
    for _ in range(20):
        arrows = Arrows()
        arrows_sprites.add(arrows)
    waiting = True
    while waiting:
        clock.tick(FPS)  # Control FPS 
        WIN.fill(BLACK)  # White background
        arrows_sprites.draw(WIN)
        arrows_sprites.update()
        # font = os.path.join("Assets" , "font.ttf")  # Download font from computer
        draw_text("Welcome to Arrow Game!" , os.path.join("Assets" , "Courier.ttf") , 40 , WIDTH/2 , HEIGHT/3 , WHITE)
        draw_text("Use arrow key to eliminate arrows" , os.path.join("Assets" , "Courier.ttf") , 35 , WIDTH/2 , HEIGHT/2 , GREEN)
        draw_text("Press Enter to start" , os.path.join("Assets" , "Courier.ttf") , 30 , WIDTH/2 , HEIGHT*2/3 , WHITE)
        draw_text("(Press Space to pause)" , os.path.join("Assets" , "Courier.ttf") , 25 , WIDTH/2 , HEIGHT*7/9 , WHITE)
        draw_text("F11 : Full Screen" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIDTH - 100 , 80 , WHITE)
        draw_text("Esc : End the game" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIDTH - 100 , 120 , WHITE)
        if sound_check % 2:
            WIN.blit(UNMUTE_WHITE , (WIDTH - UNMUTE.get_rect().width - 15 , 10))
        else:
            WIN.blit(MUTE_WHITE , (WIDTH - MUTE.get_rect().width - 15 , 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_F11:
                    if F11_times % 2:
                        WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w - 700 , WIN_RESOLUTIONS.current_h - 110  #900 , 1000
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                        unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  
                        pygame.mouse.set_visible(True)
                    else:
                        WIDTH , HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                        unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  
                        pygame.mouse.set_visible(False)
                    F11_times += 1 
                    
            if event.type == pygame.VIDEORESIZE:
                WIDTH , HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and unmute_pos.left < mouse_x < unmute_pos.right and unmute_pos.top < mouse_y < unmute_pos.bottom:
                    sound_check += 1
                    if sound_check % 2:
                        PAUSE_SOUND.set_volume(0.4)
                        PRESS_SOUND.set_volume(0.5)
                        pygame.mixer.music.unpause()
                        # pygame.mixer.music.set_volume(0.2)
                    else:
                        PAUSE_SOUND.set_volume(0)
                        PRESS_SOUND.set_volume(0)
                        pygame.mixer.music.pause()
                        # pygame.mixer.music.set_volume(0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # waiting = False
                    return False

def draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites):
    global WIN , WIDTH , HEIGHT , F11_times , record
    """ 
    try:
        with open(os.path.join("Assets" , "Record.txt") , 'r') as f:
            try:
                record = int(f.read())
            except:
                record = 0
    except:
        record = 0 
    """
    SOCLOSE = False
    NEWRECORD = False
    if record - 2 <= SCORE <= record:
        SOCLOSE = True
    elif record < SCORE:
        NEWRECORD = True
        with open(os.path.join("Assets" , "Record.txt") , 'w') as f1:
            f1.write(str(SCORE))
        record = SCORE
    waiting = True
    while waiting:
        clock.tick(FPS)  # Control FPS 

        WIN.fill(WHITE)  # White background
        pygame.draw.rect(WIN , Turquoise , (0,0 , WIDTH/2 - ARROWS_WIDTH/2,HEIGHT))  # background of tow sides
        pygame.draw.rect(WIN , Turquoise , (WIDTH/2 + ARROWS_WIDTH/2,0 , WIDTH - (WIDTH/2 + ARROWS_WIDTH/2),HEIGHT))  # background of tow sides
        # Draw scores text #
        main_font = pygame.font.Font(os.path.join("Assets" , "ComicSansMS3.ttf") , 30)
        render_text = main_font.render(f"Arrows : {SCORE}" , 1 , BLACK)
        WIN.blit(render_text , (10,10))
        # Draw scores text #
        all_sprites.draw(WIN)

        if record:
            # Draw record #
            main_font = pygame.font.Font(os.path.join("Assets" , "ComicSansMS3.ttf") , 30)
            render_text = main_font.render(f"Record : {record}" , 1 , BLACK)
            WIN.blit(render_text , (12,50))
            # Draw record #
        draw_text(f"You eliminated {SCORE} arrows !" , os.path.join("Assets" , "Courier.ttf") , 45 , WIDTH/2 , HEIGHT/2 , BLUE , 1)
        draw_text("Press Enter to play again" , os.path.join("Assets" , "Courier.ttf") , 35 , WIDTH/2 , HEIGHT*3/4 , BLUE , 1)
        if SOCLOSE:
            draw_text("So close to break the record :(" , os.path.join("Assets" , "Courier.ttf") , 40 , WIDTH/2 , HEIGHT/4 , RED , 1)
        if NEWRECORD:
            draw_text("New Record !" , os.path.join("Assets" , "Courier.ttf") , 50 , WIDTH/2 , HEIGHT/4 , RED , 1)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_F11:
                    if F11_times % 2:
                        WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w - 700 , WIN_RESOLUTIONS.current_h - 110 #900 , 1000
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                        pygame.mouse.set_visible(True)
                    else:
                        WIDTH , HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                        pygame.mouse.set_visible(False)
                    F11_times += 1 
                    for sprite in all_sprites:  # Update sprites' centerx
                        sprite.rect.centerx = WIDTH/2
                    draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)

            if event.type == pygame.VIDEORESIZE:
                WIDTH , HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                for sprite in all_sprites: 
                    sprite.rect.centerx = WIDTH/2
                draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # waiting = False
                    return False
   
def pause(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites):
    global WIN , WIDTH , HEIGHT , pause_state , on_or_off , F11_times , sound_check , unmute_pos
    waiting = True
    while waiting:
        clock.tick(FPS)  # Control FPS 
        pygame.draw.rect(WIN , Turquoise , (WIDTH/2 + ARROWS_WIDTH/2,0 , WIDTH - (WIDTH/2 + ARROWS_WIDTH/2),HEIGHT))  # Redraw right side background to update mute or unmute
        draw_text("Pause" , os.path.join("Assets" , "Courier.ttf") , 100 , WIDTH/2 , HEIGHT/2 , RED , 3)
        draw_text("F11 : Full Screen" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIDTH - 100 , 80 , BLACK)
        draw_text("Esc : End the game" , os.path.join("Assets" , "ComicSansMS3.ttf") , 20 , WIDTH - 100 , 120 , BLACK)
        if sound_check % 2:
            WIN.blit(UNMUTE , (WIDTH - UNMUTE.get_rect().width - 15 , 10))
        else:
            WIN.blit(MUTE , (WIDTH - MUTE.get_rect().width - 15 , 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == pygame.K_F11:
                    if F11_times % 2:
                        WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w - 700 , WIN_RESOLUTIONS.current_h - 110  #900 , 1000
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                        unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)
                        pygame.mouse.set_visible(True)
                    else:
                        WIDTH , HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                        unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)
                        pygame.mouse.set_visible(False)
                    F11_times += 1 
                    for sprite in all_sprites:  # Update sprites' centerx
                        sprite.rect.centerx = WIDTH/2
                    draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)

            if event.type == pygame.VIDEORESIZE:
                WIDTH , HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                unmute_pos = pygame.Rect(WIDTH - UNMUTE.get_rect().width - 15 , 10 , UNMUTE.get_rect().width , UNMUTE.get_rect().height)  
                for sprite in all_sprites: 
                    sprite.rect.centerx = WIDTH/2
                draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_state = on_or_off[0]
                    on_or_off.reverse()
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and unmute_pos.left < mouse_x < unmute_pos.right and unmute_pos.top < mouse_y < unmute_pos.bottom:
                    sound_check += 1
                    if sound_check % 2:
                        PAUSE_SOUND.set_volume(0.4)
                        PRESS_SOUND.set_volume(0.5)
                        pygame.mixer.music.unpause()
                        # pygame.mixer.music.set_volume(0.2)
                    else:
                        PAUSE_SOUND.set_volume(0)
                        PRESS_SOUND.set_volume(0)
                        pygame.mixer.music.pause()
                        # pygame.mixer.music.set_volume(0)

def change_velocity(SCORE=0 , VELOCITY=3):
    if SCORE == 5:
        VELOCITY = 4
    elif SCORE == 20:
        VELOCITY = 5
    elif SCORE == 35:
        VELOCITY = 6
    elif SCORE == 50:
        VELOCITY = 7
    elif SCORE == 100:
        VELOCITY = 8
    elif SCORE == 200:
        VELOCITY = 9
    elif SCORE == 500:
        VELOCITY = 10
    elif SCORE == 1000:
        VELOCITY = 11
    elif SCORE == 2000:
        VELOCITY = 12
    return SCORE , VELOCITY


def main(show):
    global WIN , WIDTH , HEIGHT , pause_state , on_or_off , F11_times
    run = True
    init_show = show
    SCORE = 0
    VELOCITY = 3

    all_sprites = pygame.sprite.Group()  # Create sprites group
    ARROWS_LINE_NUMBER = []

    while run:
        if init_show:
            close = draw_init_screen()
            if close:
                return True
            init_show = False
        clock.tick(FPS)  # Control FPS 
        if len(all_sprites.sprites()) >= 1 and all_sprites.sprites()[0].rect.top >= HEIGHT:
            fail = draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
            if fail:
                return True
            else:
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return True

            if event.type == pygame.VIDEORESIZE:
                WIDTH , HEIGHT = event.w , event.h
                WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                for sprite in all_sprites:  # Update sprites' centerx
                    sprite.rect.centerx = WIDTH/2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return True

                if event.key == pygame.K_F11:
                    if F11_times % 2:
                        WIDTH , HEIGHT = WIN_RESOLUTIONS.current_w - 700 , WIN_RESOLUTIONS.current_h - 110  #900 , 1000
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.RESIZABLE)
                        pygame.mouse.set_visible(True)
                    else:
                        WIDTH , HEIGHT  = WIN_RESOLUTIONS.current_w , WIN_RESOLUTIONS.current_h
                        WIN = pygame.display.set_mode((WIDTH, HEIGHT) , pygame.FULLSCREEN | pygame.NOFRAME)
                        pygame.mouse.set_visible(False)
                    F11_times += 1 
                    for sprite in all_sprites:  # Update sprites' centerx
                        sprite.rect.centerx = WIDTH/2

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    PRESS_SOUND.play()
                    if ARROWS_LINE_NUMBER[0] == 0:
                        all_sprites.remove(all_sprites.sprites()[0])
                        ARROWS_LINE_NUMBER.pop(0)
                        SCORE += 1
                    else:
                        fail = draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
                        if fail:
                            return True
                        else:
                            run = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    PRESS_SOUND.play()
                    if ARROWS_LINE_NUMBER[0] == 1:
                        all_sprites.remove(all_sprites.sprites()[0])
                        ARROWS_LINE_NUMBER.pop(0)
                        SCORE += 1
                    else:
                        fail = draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
                        if fail:
                            return True
                        else:
                            run = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    PRESS_SOUND.play()
                    if ARROWS_LINE_NUMBER[0] == 2:
                        all_sprites.remove(all_sprites.sprites()[0])
                        ARROWS_LINE_NUMBER.pop(0)
                        SCORE += 1
                    else:
                        fail = draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
                        if fail:
                            return True
                        else:
                            run = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    PRESS_SOUND.play()
                    if ARROWS_LINE_NUMBER[0] == 3:
                        all_sprites.remove(all_sprites.sprites()[0])
                        ARROWS_LINE_NUMBER.pop(0)
                        SCORE += 1
                    else:
                        fail = draw_failure(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
                        if fail:
                            return True
                        else:
                            run = False
                if event.key == pygame.K_SPACE:
                    PAUSE_SOUND.play()
                    pause_state = on_or_off[0]
                    on_or_off.reverse()

        if pause_state:
            pause_game = pause(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
            if pause_game:
                return True 
        else:
            SCORE , VELOCITY = change_velocity(SCORE , VELOCITY)
            draw_window(SCORE , VELOCITY , ARROWS_LINE_NUMBER , all_sprites)
    
    main(False)


if __name__ == "__main__":
    quit = main(True)
    if quit:
        pygame.quit()