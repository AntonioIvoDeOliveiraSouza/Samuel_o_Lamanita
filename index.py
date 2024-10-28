# Samuel o Lamanita - o jogo [Samuel the lamanite -  the game]
# Developed by Antonio Ivo
# Created in 02/08/2024
# Follow me on github to new updates

# What to add:
# * English option
# * New levels (How?)
# 10 Níveis - 3 corações
# Cada cidade, uma história nova
# Flechas devagar e menos trechos
# Resolver Intro


#Importing libraries
#from pyvidplayer2 import Video
import pygame
from pygame.locals import *
from random import *
import sys
import random
import time

# Menu var
running = True
global soundMute
soundMute = True

# Iniatilizing some tools
pygame.display.init()
pygame.init()
pygame.font.init()

# Initializing button
#button class - that's how the buttons work
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# Initializing font
font = pygame.font.Font("font/Aztec.ttf", 20)

# Initializing font color
AV_BLACK = (0, 0, 0)
AV_WHITE = (255, 255, 255)

# screen configurations - 576x576
screen_size = (576, 576)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Samuel o Lamanita")
icon = pygame.image.load("sprites/icons/scroll.png")
pygame.display.set_icon(icon)

#LOADING VIDEO
#introVideo = Video("video/jumento_intro.mp4")   
#introVideo.resize((576,576))

#INTRO FUNCTION
#def intro():
    #introVideo.play()

    #t = 5
    #while t:
        #introVideo.draw(screen,(0,0))
        #pygame.display.flip()

        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
            #if event.type == MOUSEBUTTONDOWN:
                #introVideo.close()
                #menu(soundMute)
            #if t == 0:
                #introVideo.close()
                #menu(soundMute)
            #t-=0.4
        #time.sleep(0.5)



# draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Game function
def game(soundMute):

    #==========Initializing speak image=============#
    speak_sprites = []
    speak_sprites = [pygame.image.load(f"sprites/speak/{i}.png") for i in range(1, 58)]

    show_speak = True
    speak_timer = 0
    speak_image = None
    #==========End of speak initializer=============#

    collision_detected = False
    scroll_positions = [(0,320),(100,320),(200,320),(300,320),(400,320),(500,320)] 

    #Creating Class Scroll
    class Scroll (pygame.sprite.Sprite):
        def __init__(self):
            self.sprites = []
            pygame.sprite.Sprite.__init__(self)
            self.sprites.append(pygame.image.load("sprites/icons/scroll.png"))
            self.atual = 0
            self.image = self.sprites[0]

            self.rect = self.image.get_rect()
            self.rect.topleft = choice(scroll_positions)
            self.image = pygame.transform.scale(self.image, (47,49))

        def update(self):
                self.animate = True
                self.atual = self.atual + 1
                if self.atual >= len(self.sprites):
                    self.atual =  0
                    self.animate = False
                self.image = self.sprites[int(self.atual)]   
                self.image = pygame.transform.scale(self.image, (47,49)) 

    #===============Initializing arrow class==========================#
    class Arrow(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.sprites = [pygame.image.load("sprites/icons/arrow.png")]
            self.atual = 0
            self.image = pygame.transform.scale(self.sprites[0], (37, 39)) #47,49
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, 576 - 131)
            self.rect.topleft = (self.rect.x, 0)
            self.speed = 3
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.rect.y += self.speed
            if self.rect.y > 576:
                self.rect.x = random.randint(0, 576 - 131)
                self.rect.y = -576
            self.mask = pygame.mask.from_surface(self.image)  # Changes the arrow position

        #def draw(self, screen):
            #screen.blit(self.image, self.rect)
            #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            #To visualize the screen (opcional)

    arrows = pygame.sprite.Group()
    initial_arrow_count = 1
    for _ in range(initial_arrow_count):
        arrow = Arrow()
        arrows.add(arrow)    

    #================Ending arrow class============================#
    #===============Class Sam======================#
    class Sam(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.sprites_left = [pygame.image.load(f"sprites/sam/walk_left/walkLeft_{i}.png") for i in range(0, 4)]
            self.sprites_right = [pygame.image.load(f"sprites/sam/walk_right/walkRight_{i}.png") for i in range(0, 4)]
            self.atual = 0
            self.image = pygame.transform.scale(self.sprites_right[0], (66, 77))
            self.rect = self.image.get_rect()
            self.rect.topleft = 300, 280
            self.animate = False
            self.speed = 5
            self.direction = "right"
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            if self.animate:
                self.atual += 0.4
                if self.atual >= len(self.sprites_right):
                    self.atual = 0
                    self.animate = False

                if self.direction == "right":
                    self.image = self.sprites_right[int(self.atual)]
                    self.rect.x += self.speed
                else:
                    self.image = self.sprites_left[int(self.atual)]
                    self.rect.x -= self.speed
                self.image = pygame.transform.scale(self.image, (77,88))
                self.mask = pygame.mask.from_surface(self.image)

                if self.rect.left <= -50:
                    self.rect.left = -50
                if self.rect.right >= 626:
                    self.rect.right = 626

        def moveRight(self):
            self.direction = "right"
            self.animate = True

        def moveLeft(self):
            self.direction = "left"
            self.animate = True

        def stop(self):
            self.animate = False

#====================End of sam Class=======================================#
            
    all_sprites = pygame.sprite.Group()
    sam = Sam()
    scroll = Scroll()
    all_sprites.add(sam)
    all_sprites.add(scroll)

    timer = pygame.time.Clock()

#======================== main code start =========================#
    running = True
    count = 0 #Count to speak appear in order
    print("Game started!")

    #=========message score point===============#
    score_point = 0
    score_font = pygame.font.Font('font/Aztec.ttf',30)

    score_path = "img/score.png"
    score = pygame.image.load(score_path)
    score = pygame.transform.scale(score, (500*0.5,500*0.5))
    #====message score point initializer end====#

    background_path = "img/bg_01.jpg"
    background = pygame.image.load(background_path)

    #===== Game music initializer =====#
    if (soundMute):
        collect_sound = pygame.mixer.Sound("sound/collect_sound.wav")
    pygame.mixer.music.load("sound/game_music.mp3")
    pygame.mixer.music.play(-1)
    if (soundMute):
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.0)

    while running:
        timer.tick(30) #Timer to change the sprite
        score_msg = f'score : {score_point}' 
        formated_score_msg = score_font.render(score_msg, True, (0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[K_d] or key[K_RIGHT]: #Some key is pressed
            sam.moveRight()
        elif key[K_a] or key[K_LEFT]:
            sam.moveLeft()

        arrows.update()

        new_arrow_probability = 0.01
        if random.random() < new_arrow_probability:  # Arrow probability 
            arrow = Arrow()
            arrows.add(arrow)

        screen.fill((0,0,0))
        screen.blit(background,(0,0))   
        screen.blit(score,(325, -85))
        screen.blit(formated_score_msg,(365,33))
        all_sprites.draw(screen)
        all_sprites.update()   
        arrows.draw(screen)

        # =============== Colision - sam/arrow  ============== # Problem
        for arrow in arrows:    
            #arrow.draw(screen)
            offset = (arrow.rect.left - sam.rect.left, arrow.rect.top - sam.rect.top)
            if sam.mask.overlap(arrow.mask, offset):
                print("Colisão entre Sam e uma Arrow detectada! - Game over")
                screen.fill((0,0,0))
                game_over(score_point,soundMute)
                arrows.remove(arrow)
            
        # =============== Colision - sam/scroll ============== #

        if pygame.sprite.collide_rect(sam, scroll):
            if not collision_detected:
                print("Colisão detectada!")
                score_point = score_point + 1
                last_pos = scroll.rect.topleft
                while last_pos == scroll.rect.topleft:
                    scroll.rect.topleft = choice(scroll_positions) #Scroll changes position

                #=======Speak appear first in order, then it became random =======#
                show_speak = True
                speak_timer = pygame.time.get_ticks()
                if count<=58:
                    speak_count = 0+count
                    speak_image = speak_sprites[0+speak_count]
                    speak_image = pygame.transform.scale(speak_image, (500*0.3,500*0.3))
                    count +=1
                else: #All the sprites appeared, then became random
                    speak_image = choice(speak_sprites)
                    speak_image = pygame.transform.scale(speak_image, (500*0.3,500*0.3))

                if (soundMute):
                    collect_sound.play() #sound play
                else:
                    pass

                collision_detected = True
        else:
            collision_detected = False  # When there isn't colision - resets the var
        #========== Verify the speak ===========#
        if show_speak:
            if speak_image:
                if pygame.time.get_ticks() - speak_timer < 3000: #5 seconds
                    if scroll.rect.left == 500: #It's based on scroll position
                        screen.blit(speak_image, (scroll.rect.left-50, scroll.rect.top - speak_image.get_height()))
                    elif scroll.rect.left == 0:
                        screen.blit(speak_image, (scroll.rect.left+50, scroll.rect.top - speak_image.get_height()))
                    else:
                        screen.blit(speak_image, (scroll.rect.left, scroll.rect.top - speak_image.get_height()))
                else:
                    show_speak = False
        
        pygame.display.flip()      

# Function game over
def game_over(score_point,soundMute):
    
    pygame.mixer.music.load("sound/gameover_music.mp3")
    pygame.mixer.music.play(-1)

    if (soundMute):
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.0)

    resume = True

    score_board_path = "img/score.png"
    score_board = pygame.image.load(score_board_path) 
    score_board = pygame.transform.scale(score_board, (500*0.5,500*0.5))

    gameOver_bg_path = "img/game_over.png"
    gameOver_bg = pygame.image.load(gameOver_bg_path)

    while resume:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    menu(soundMute)
    
        screen.fill((0,0,0))
        screen.blit(gameOver_bg,(0,0))
        draw_text("Pressione X para voltar ao menu",font,AV_WHITE,115,400)
        screen.blit(score_board,(150,350))
        draw_text(f'SCORE: {score_point}',font, AV_BLACK,180,473)
        pygame.display.flip()

# Instruction game function
def instruction_game(bgMenu, yesButtonImg,soundMute):

    if (soundMute):
        soundMute = True
    else:
        soundMute = False

    resume = True

    #calling message image
    instImg_path = "img/inst_game.png"
    instImg = pygame.image.load(instImg_path)

    yesButton = Button(475,500,yesButtonImg,1)

    while resume:
    #Inicializing start - instructions and explanation
    #first screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if yesButton.draw(screen):
            #Calls the game function:
                screen.fill((0, 0, 0))
                start_game(bgMenu,yesButtonImg,soundMute)

        screen.fill((0, 0, 0))
        screen.blit(bgMenu,(0,0))
        screen.blit(instImg,(50,0))
        yesButton.draw(screen)
        pygame.display.flip()

# Story game
def start_game(bgMenu,yesButtonImg,soundMute):
    print("Jogo iniciado!")

    if (soundMute):
        soundMute = True
    else:
        soundMute = False

    resume = True

    #calling message image
    msgImg_path = "img/msg_game.png"
    msgImg = pygame.image.load(msgImg_path)

    helama_path = "img/helama.png"
    helama_img = pygame.image.load(helama_path)
    helama_img = pygame.transform.scale(helama_img,(500*0.7,500*0.7))

    yesButton = Button(475,500,yesButtonImg,1)

    while resume:
        #Inicializing start - game explanation
        #first screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se clicar em sair da janela (no X)
                pygame.quit()
                sys.exit()
            if yesButton.draw(screen):
                #Calls the game function
                game(soundMute)

        #Zona de construção
        screen.fill((0, 0, 0))
        screen.blit(bgMenu,(0,0))
        screen.blit(msgImg,(50,0))
        screen.blit(helama_img,(0,330))
        yesButton.draw(screen)
        pygame.display.flip()

# Option function
def option_game(bgMenu,title,backButtonImg,soundMute):    

    #Creating mute button:
    muteImg_path = "img/mute.png"
    muteImg = pygame.image.load(muteImg_path)
    muteButton = Button(300, 200, muteImg, 1)

    pygame.mixer.music.load("sound/outro_music.mp3")
    pygame.mixer.music.play(-1)

    if (soundMute):
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.0)

    print("Option selecionado!")
    resume = True

    backButton = Button(-20,500,backButtonImg,1)
    title = pygame.transform.scale(title, (200,200))

    while resume:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
          if backButton.draw(screen):
             menu(soundMute)
          if muteButton.draw(screen):
              if (soundMute):
                soundMute = False
                print("Som mutado!")
                pygame.mixer.music.set_volume(0.0)
              else:
                  soundMute = True
                  print("Som ligado!")
                  pygame.mixer.music.set_volume(0.5)

        screen.fill((0, 0, 0))
        screen.blit(bgMenu,(0,0))
        muteButton.draw(screen)    
        backButton.draw(screen)
        screen.blit(title,(0,0))

        draw_text("DESATIVAR/ATIVAR SOM", font, AV_BLACK, 90, 225)

        pygame.display.flip()

#About screen
def about_game(bgMenu,title,backButtonImg,soundMute):    

    print("About selecionado!")
    resume = True

    pygame.mixer.music.load("sound/outro_music.mp3")
    pygame.mixer.music.play(-1)
    if (soundMute):
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.0)

    aboutImg_path = "img/msg_sobre.png"
    sobre_img = pygame.image.load(aboutImg_path)

    backButton = Button(-20,500,backButtonImg,1)
    title = pygame.transform.scale(title, (200,200)) 

    while resume:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if backButton.draw(screen):
                menu(soundMute)

        screen.fill((0, 0, 0))
        screen.blit(bgMenu,(0,0))
        
        backButton.draw(screen)
        screen.blit(title,(0,-27))

        screen.blit(sobre_img,(0,50))

        pygame.display.flip()

# Function menu
def menu(soundMute):

    global running  # Global var running

    #01. Menu Background
    bgMenu_path = "img/background.png"
    bgMenu = pygame.image.load(bgMenu_path)
    bgMenu_pos = (0, 0)

    #02. title
    title_path = "img/title.png"
    title = pygame.image.load(title_path)
    title_pos = (150, -50)

    #03. Start button
    startButton_path = "img/start.png"
    startButtonImg = pygame.image.load(startButton_path)

    #04. About button
    aboutButton_path = "img/about.png"
    aboutButtonImg = pygame.image.load(aboutButton_path)

    #05. Exit button
    exitButton_path = "img/exit.png"
    exitButtonImg = pygame.image.load(exitButton_path)

    #06. Option button
    optionButton_path = "img/option.png"
    optionButtonImg = pygame.image.load(optionButton_path)

    #07. Back button
    buttonBack_path = "img/back.png"
    backButtonImg = pygame.image.load(buttonBack_path)

    #08. Yes button
    buttonYes_path = "img/yes.png"
    yesButtonImg = pygame.image.load(buttonYes_path)

    # Instância dos botões
    startButton = Button(225, 225, startButtonImg, 1)
    optionButton = Button(225, 300, optionButtonImg, 1)
    aboutButton = Button(225,375,aboutButtonImg,1)
    exitButton = Button(225, 450, exitButtonImg, 1)

    pygame.mixer.music.load("sound/menu_music.mp3")
    pygame.mixer.music.play(-1)
    if (soundMute):
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0.0)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        if startButton.draw(screen):
            instruction_game(bgMenu,yesButtonImg,soundMute)
        elif optionButton.draw(screen):
            option_game(bgMenu,title,backButtonImg,soundMute)
        elif aboutButton.draw(screen):
            about_game(bgMenu,title,backButtonImg,soundMute)
        elif exitButton.draw(screen):
            pygame.quit()
            sys.exit()

        screen.fill((0, 0, 0))  
        screen.blit(bgMenu, bgMenu_pos) 
        screen.blit(title,title_pos) 
        startButton.draw(screen)
        optionButton.draw(screen)
        aboutButton.draw(screen)
        exitButton.draw(screen)

        draw_text("Feito por Antonio Ivo", font, AV_BLACK, 0, 550)
        draw_text("Versão 1.0.1", font, AV_BLACK, 450, 550)
        pygame.display.flip() 

#recursivity
#intro()
menu(soundMute)

# Leaving the game
pygame.quit()
sys.exit()