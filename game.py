import random
import pygame
import sys
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_ong():
    random_ong_pos = random.choice(ong_height)
    duoi_ong = ong_xanh.get_rect(midtop=(500, random_ong_pos))
    tren_ong = ong_xanh.get_rect(midtop=(500, random_ong_pos - 650))
    return {'duoi': duoi_ong, 'tren': tren_ong, 'scored': False}
def move_ong(ongs):
    for ong in ongs:
        ong['duoi'].centerx -= 5
        ong['tren'].centerx -= 5
    return [ong for ong in ongs if ong['duoi'].right > 0]
def draw_ong(ongs):
    for ong in ongs:
        screen.blit(ong_xanh, ong['duoi'])
        flip_ong = pygame.transform.flip(ong_xanh, False, True)
        screen.blit(flip_ong, ong['tren'])
def check_collsion(ongs):
    for ong in ongs:
        if bird_rect.colliderect(ong):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
def rotate_bird(chim):
    new_bird = pygame.transform.rotozoom(chim, -bird_movemet*3, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect= new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,625))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
gravity = 0.25
bird_movemet = 0
game_active = True
score = 0
high_score = 0
bg = pygame.image.load('assests/background-night.png')
bg = pygame.transform.scale2x(bg)
floor = pygame.image.load('assests/floor.png')
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('assests/yellowbird-midflap.png')
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)
ong_xanh = pygame.image.load('assests/pipe-green.png')
ong_xanh = pygame.transform.scale2x(ong_xanh)
ong_list = []
spawpipe = pygame.USEREVENT
pygame.time.set_timer(spawpipe,1200)
ong_height = [200,300,400]
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#score_sound_countdown = 100
game_state = "start"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == "start":
                game_state = "main game"  # Bắt đầu chơi game
            elif game_state == "game over":
                game_state = "start"  # Quay lại màn hình Start
            if event.key == pygame.K_SPACE and game_active:
                bird_movemet = 0
                bird_movemet = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                ong_list.clear()
                bird_rect.center = (100,384)
                bird_movemet = 0
                score = 0
        if event.type == spawpipe:
            ong_list.append(create_ong())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(bg,(0,0))
    if game_state == "start":
        # Hiển thị màn hình Start với hình `message.png`
        screen.blit(game_over_surface, (70, 174))  # Vị trí hiển thị hình ảnh
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                score_display(game_state)   
        #start_text = game_font.render("Press SPACE to Start", True, (255, 255, 255))
        #start_text_rect = start_text.get_rect(center=(216, 650))
        #screen.blit(start_text, start_text_rect)
    
    if game_active:
        bird_movemet += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movemet
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collsion(
            [ong['duoi'] for ong in ong_list] + [ong['tren'] for ong in ong_list])
        #if not game_active:
            #game_state = "game over"  # Chuyển sang trạng thái Game Over
        ong_list = move_ong(ong_list)
        draw_ong(ong_list)
        for ong in ong_list:
            if ong['duoi'].centerx < bird_rect.centerx and not ong['scored']:
                score += 1
                ong['scored'] = True
                score_sound.play()
        score_display('main game')
            #score_sound_countdown -= 1
            #if score_sound_countdown <= 0:
                #score_sound.play()
                #score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)