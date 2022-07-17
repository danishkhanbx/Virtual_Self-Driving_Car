import pygame

pygame.init()

window = pygame.display.set_mode((1200, 400))

pygame.display.set_caption('Tesla')
Icon = pygame.image.load('tesla_logo_PNG16.png')
pygame.display.set_icon(Icon)

track = pygame.image.load('track6.png')
car = pygame.image.load('tesla.png')
car = pygame.transform.scale(car, (30, 60))  # cars starting position
car_x = 150
car_y = 300

focal_dis = 25    # cameras range
cam_x_offset = 0  # we need to offset cameras (x, y) coordinates when it takes a turn
cam_y_offset = 0

direction = 'up'

clock = pygame.time.Clock()

drive = True
while drive:
    for event in pygame.event.get():  # when clicked quit X button
        if event.type == pygame.QUIT:
            drive = False

    clock.tick(60)                     # speed of the car

    cam_x = car_x + cam_x_offset + 15  # cameras moving with car, only needed in case of virtual
    cam_y = car_y + cam_y_offset + 15

    up_px = window.get_at((cam_x, cam_y - focal_dis))[0]     # upper pixel, pixel value at the front of the car from the cameras range
    right_px = window.get_at((cam_x + focal_dis, cam_y))[0]  # right pixel, pixel value at the right of the car from the cameras range
    left_px = window.get_at((cam_x - focal_dis, cam_y))[0]   # left pixel, pixel value at the right of the car from the cameras range
    down_px = window.get_at((cam_x, cam_y + focal_dis))[0]   # down pixel, pixel value at the front of the car from the cameras range
    print(up_px, right_px, down_px)

    # change direction ( taking a turn)
    # Similarly, we can do the up->left,up->down, down->up,down->left, left->right,left->up,left->down, right->left
    if direction == 'up' and up_px != 255 and right_px == 255:         # means upward road ends, and there is a road on the right side
        direction = 'right'
        cam_x_offset = 30
        car = pygame.transform.rotate(car, -90)
    elif direction == 'right' and right_px != 255 and down_px == 255:  # road on the right ends, and there is a road on the down side
        direction = 'down'
        car_x = car_x + 30
        cam_x_offset = 0
        cam_y_offset = 30
        car = pygame.transform.rotate(car, -90)
    elif direction == 'down' and down_px != 255 and right_px == 255:   # means downward road ends, and there is a road on the right side
        direction = 'right'
        car_y = car_y + 30
        cam_x_offset = 30
        cam_y_offset = 0
        car = pygame.transform.rotate(car, 90)
    elif direction == 'right' and right_px != 255 and up_px == 255:    # means downward road ends, and there is a road on the right side
        direction = 'up'
        car_x = car_x + 30
        cam_x_offset = 0
        car = pygame.transform.rotate(car, 90)

    # driving direction
    if direction == 'up' and up_px == 255:          # when we are going in the upwards direction ,if the camera detects white road then only we move
        car_y = car_y - 2  # moving up in direction
    elif direction == 'right' and right_px == 255:  # when we are going in the right direction ,if the camera detects white road then only we move
        car_x = car_x + 2  # moving in the right direction
    elif direction == 'down' and down_px == 255:    # when we are going in the down direction ,if the camera detects white road then only we move
        car_y = car_y + 2  # moving in the down direction
    elif direction == 'left' and left_px == 255:    # when we are going in the left direction ,if the camera detects white road then only we move
        car_x = car_x - 2  # moving in the down direction

    window.blit(track, (0, 0))   # BLock Image Transfer, showing track and car in the output
    window.blit(car, (car_x, car_y))

    pygame.draw.circle(window, (0, 255, 0), (cam_x, cam_y), 3, 3)  # showing camera on the car

    pygame.display.update()
