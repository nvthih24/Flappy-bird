import pygame
import sys

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

pygame.init()

# Cài đặt màn hình và FPS
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# Tải hình ảnh
bg = pygame.image.load('assests/background-night.png')
bg = pygame.transform.scale2x(bg)
floor = pygame.image.load('assests/floor.png')
floor = pygame.transform.scale2x(floor)
start_screen_img = pygame.image.load('assests/message.png')
start_screen_img = pygame.transform.scale2x(start_screen_img)

# Biến game
game_state = "start"
floor_x_pos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "main"  # Bắt đầu chơi game
                elif game_state == "game over":
                    game_state = "start"  # Quay lại màn hình Start

    screen.blit(bg, (0, 0))  # Hiển thị nền

    if game_state == "start":
        # Hiển thị màn hình Start với hình `message.png`
        screen.blit(start_screen_img, (108, 200))  # Vị trí hiển thị hình ảnh
        start_text = game_font.render("Press SPACE to Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(216, 650))
        screen.blit(start_text, start_text_rect)
    
    elif game_state == "main":
        # Thêm logic chính của game vào đây
        pass

    elif game_state == "game over":
        # Hiển thị màn hình Game Over (nếu cần)
        pass

    # Vẽ sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
