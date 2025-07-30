#
Overview
##
This library provides an easy-to-use `SpriteAnimation` class for Pygame that handles sprite sheet animations. It allows you to animate 2D characters or objects using a sprite sheet made up of equal-sized frames.

###
Key Features
###
- Loads animations from a sprite sheet using customizable frame size
- Automatically handles frame timing and animation playback
- Supports looping and one-shot animations
- Allows optional frame scaling to a new size
- Supports horizontal flipping of animations
- Easily reset animations at any time

####
Basic Usage
####

from sprite_animation import SpriteAnimation
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

#Create animation
anim = SpriteAnimation("spritesheet.png", frame_size=(32, 32), frame_duration=100, final_size=(64, 64))

#Main loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60)  #Ms since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    anim.update(dt)
    
    screen.fill((0, 0, 0))
    anim.draw(screen, (100, 100))
    pygame.display.flip()

pygame.quit()
