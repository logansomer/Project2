import random
import pygame
from sys import exit
from random import randint, choice

current_time = 0
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_role_1 = pygame.image.load('Graphics\player\player_walk_1.png').convert_alpha()
        player_role_1_5 = pygame.image.load('Graphics\player\player_walk_1.5.png').convert_alpha()
        player_role_2 = pygame.image.load('Graphics\player\player_walk_2.png').convert_alpha()
        player_role_2_5 = pygame.image.load('Graphics\player\player_walk_2.5.png').convert_alpha()
        player_role_3 = pygame.image.load('Graphics\player\player_walk_3.png').convert_alpha()
        player_role_3_5 = pygame.image.load('Graphics\player\player_walk_3.5.png').convert_alpha()
        player_role_4 = pygame.image.load('Graphics\player\player_walk_4.png').convert_alpha()
        player_role_4_5 = pygame.image.load('Graphics\player\player_walk_4.5.png').convert_alpha()


        self.player_role = [player_role_1,player_role_1_5, player_role_2,player_role_2_5, player_role_3,player_role_3_5, player_role_4,player_role_4_5]
        self.player_index = 0
        self.player_jump = pygame.image.load('Graphics\player\jump1.png').convert_alpha()


        self.image = self.player_role[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('graphics/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -9
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
        if self.rect.top <= 0:
            self.rect.top = 0

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_role):self.player_index = 0
            self.image = self.player_role[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'knife':
            knife_1 = pygame.image.load('Graphics/knife/knife1.png').convert_alpha()
            knife_2 = pygame.image.load('Graphics/knife/knife2.png').convert_alpha()
            self.frames = [knife_1,knife_2]
            y_pos = random.randint(3,216)
        else:
            toaster_1 = pygame.image.load('Graphics/toaster/toaster1.png').convert_alpha()
            toaster_2 = pygame.image.load('Graphics/toaster/toaster2.png').convert_alpha()
            self.frames = [toaster_1, toaster_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= speed
        self.destroy()
    def destroy(self):
        global current_time
        if self.rect.x <= -100:
            self.kill()
            current_time = current_time + 1


def display_score():
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rectangle = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 50

            if obstacle_rect.bottom == 300: screen.blit(toaster_surf,obstacle_rect)
            else: screen.blit(knife_surf,obstacle_rect)


            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def player_animation():
    global player_surf, player_index
    if player_rectangle.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

#display
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Bagel Escape')
clock = pygame.time.Clock()
#objects and models
test_font = pygame.font.Font('Graphics\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('graphics/music.wav')
bg_music.play(loops = -1).set_volume(0.06)
speed = 6
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Graphics\Sky.png').convert_alpha()
ground_surface = pygame.image.load('Graphics\ground.png').convert_alpha()

toaster_frame1 = pygame.image.load('Graphics/toaster/toaster1.png').convert_alpha()
toaster_frame2 = pygame.image.load('Graphics/toaster/toaster2.png').convert_alpha()
toaster_frames = [toaster_frame1,toaster_frame2]
toaster_frame_index = 0
toaster_surf = toaster_frames[toaster_frame_index]

knife_frame1 = pygame.image.load('Graphics/knife/knife1.png').convert_alpha()
knife_frame2 = pygame.image.load('Graphics/knife/knife2.png').convert_alpha()
knife_frames = [knife_frame1,knife_frame2]
knife_frame_index = 0
knife_surf = knife_frames[knife_frame_index]


obstacle_rectlist = []

player_walk_1 = pygame.image.load('Graphics\player\player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics\player\player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('Graphics\player\jump1.png').convert_alpha()

player_surf = player_walk[player_index]
player_rectangle = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro screen
player_stand = pygame.image.load('Graphics\player\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('bagel Escape:     Get 50 points to win!',False,(127,255,0))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('press space to run', False,(127,255,0))
game_message_rect = game_message.get_rect(center = (400,320))



#Timer
clock = pygame.time.Clock()
current_time = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200)

toaster_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(toaster_animation_timer,500)

knife_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(knife_animation_timer,200)

#keep display running
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
# controls
            if event.type == pygame.MOUSEBUTTONDOWN:
               if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                   player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                current_time = 0
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(obstacle(choice(['knife','knife','knife','toaster','knife','toaster'])))
            if event.type == toaster_animation_timer:
                if toaster_frame_index == 0: toaster_frame_index = 1
                else: toaster_frame_index = 0
                toaster_surf = toaster_frames[toaster_frame_index]

            if event.type == knife_animation_timer:
                if knife_frame_index == 0: knife_frame_index = 1
                else: knife_frame_index = 0
                knife_surf = knife_frames[knife_frame_index]

    if game_active:

#objects order
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()


        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

#object physics
    # collisions
        game_active = collision_sprite()

    else:
        screen.fill((59,59,59))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rectlist.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'your score: {score}',False,(127,255,0))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect,)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)
    if current_time >= 50:
        game_active = False
        screen.fill((59,59,59))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rectlist.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'YOU WIN! Score: 50',False,(127,255,0))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)



#max framerate
    pygame.display.update()
    clock.tick(60)



