# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True
dt = 0

player1_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player3_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player4_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  screen.fill("purple")
  # So here I have added the multiplayer controller implementation
  # I scaled it up already
  # Here I am working with the circle so we can change this how we need it for the
  # ghosts
  # This implamentation is for the 4 players
  # First player is keyboard untill 4 controllers are connected
  # Here I used the circle example from the front screen of pygame just scaled up some

  pygame.draw.circle(screen, "black", player4_pos, 40)
  pygame.draw.circle(screen, "blue", player3_pos, 30)
  pygame.draw.circle(screen, "white", player2_pos, 20)
  pygame.draw.circle(screen, "red", player1_pos, 10)

  joystick_count = pygame.joystick.get_count()
  print(joystick_count)

  if (joystick_count < 4):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      player1_pos.y -= 300 * dt
    if keys[pygame.K_s]:
      player1_pos.y += 300 * dt
    if keys[pygame.K_a]:
      player1_pos.x -= 300 * dt
    if keys[pygame.K_d]:
      player1_pos.x += 300 * dt
    if (joystick_count == 1):
      joystick1 = pygame.joystick.Joystick(0)
      if joystick1.get_axis(0) and joystick1.get_axis(0) < -0.2:
        player2_pos.x -= 300 * dt
      if joystick1.get_axis(0) and joystick1.get_axis(0) > 0.2:
        player2_pos.x += 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) < -0.2:
        player2_pos.y -= 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) > 0.2:
        player2_pos.y += 300 * dt
    elif (joystick_count == 2):
      joystick1 = pygame.joystick.Joystick(0)
      joystick2 = pygame.joystick.Joystick(1)
      #joystick1
      if joystick1.get_axis(0) and joystick1.get_axis(0) < -0.2:
        player2_pos.x -= 300 * dt
      if joystick1.get_axis(0) and joystick1.get_axis(0) > 0.2:
        player2_pos.x += 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) < -0.2:
        player2_pos.y -= 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) > 0.2:
        player2_pos.y += 300 * dt
      #joystick2
      if joystick2.get_axis(0) and joystick2.get_axis(0) < -0.2:
        player3_pos.x -= 300 * dt
      if joystick2.get_axis(0) and joystick2.get_axis(0) > 0.2:
        player3_pos.x += 300 * dt
      if joystick2.get_axis(1) and joystick2.get_axis(1) < -0.2:
        player3_pos.y -= 300 * dt
      if joystick2.get_axis(1) and joystick2.get_axis(1) > 0.2:
        player3_pos.y += 300 * dt
    elif (joystick_count == 3):
      joystick1 = pygame.joystick.Joystick(0)
      joystick2 = pygame.joystick.Joystick(1)
      joystick3 = pygame.joystick.Joystick(2)
      #joystick1
      if joystick1.get_axis(0) and joystick1.get_axis(0) < -0.2:
        player2_pos.x -= 300 * dt
      if joystick1.get_axis(0) and joystick1.get_axis(0) > 0.2:
        player2_pos.x += 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) < -0.2:
        player2_pos.y -= 300 * dt
      if joystick1.get_axis(1) and joystick1.get_axis(1) > 0.2:
        player2_pos.y += 300 * dt
      #joystick2
      if joystick2.get_axis(0) and joystick2.get_axis(0) < -0.2:
        player3_pos.x -= 300 * dt
      if joystick2.get_axis(0) and joystick2.get_axis(0) > 0.2:
        player3_pos.x += 300 * dt
      if joystick2.get_axis(1) and joystick2.get_axis(1) < -0.2:
        player3_pos.y -= 300 * dt
      if joystick2.get_axis(1) and joystick2.get_axis(1) > 0.2:
        player3_pos.y += 300 * dt
      #joystick3
      if joystick3.get_axis(0) and joystick3.get_axis(0) < -0.2:
        player4_pos.x -= 300 * dt
      if joystick3.get_axis(0) and joystick3.get_axis(0) > 0.2:
        player4_pos.x += 300 * dt
      if joystick3.get_axis(1) and joystick3.get_axis(1) < -0.2:
        player4_pos.y -= 300 * dt
      if joystick3.get_axis(1) and joystick3.get_axis(1) > 0.2:
        player4_pos.y += 300 * dt
  else:
    joystick1 = pygame.joystick.Joystick(0)
    joystick2 = pygame.joystick.Joystick(1)
    joystick3 = pygame.joystick.Joystick(2)
    joystick4 = pygame.joystick.Joystick(3)
    #joystick1
    if joystick1.get_axis(0) and joystick1.get_axis(0) < -0.2:
      player1_pos.x -= 300 * dt
    if joystick1.get_axis(0) and joystick1.get_axis(0) > 0.2:
      player1_pos.x += 300 * dt
    if joystick1.get_axis(1) and joystick1.get_axis(1) < -0.2:
      player1_pos.y -= 300 * dt
    if joystick1.get_axis(1) and joystick1.get_axis(1) > 0.2:
      player1_pos.y += 300 * dt
    #joystick2
    if joystick2.get_axis(0) and joystick2.get_axis(0) < -0.2:
      player2_pos.x -= 300 * dt
    if joystick2.get_axis(0) and joystick2.get_axis(0) > 0.2:
      player2_pos.x += 300 * dt
    if joystick2.get_axis(1) and joystick2.get_axis(1) < -0.2:
      player2_pos.y -= 300 * dt
    if joystick2.get_axis(1) and joystick2.get_axis(1) > 0.2:
      player2_pos.y += 300 * dt
    #joystick3
    if joystick3.get_axis(0) and joystick3.get_axis(0) < -0.2:
      player3_pos.x -= 300 * dt
    if joystick3.get_axis(0) and joystick3.get_axis(0) > 0.2:
      player3_pos.x += 300 * dt
    if joystick3.get_axis(1) and joystick3.get_axis(1) < -0.2:
      player3_pos.y -= 300 * dt
    if joystick3.get_axis(1) and joystick3.get_axis(1) > 0.2:
      player3_pos.y += 300 * dt
    #joystick4
    if joystick4.get_axis(0) and joystick4.get_axis(0) < -0.2:
      player4_pos.x -= 300 * dt
    if joystick4.get_axis(0) and joystick4.get_axis(0) > 0.2:
      player4_pos.x += 300 * dt
    if joystick4.get_axis(1) and joystick4.get_axis(1) < -0.2:
      player4_pos.y -= 300 * dt
    if joystick4.get_axis(1) and joystick4.get_axis(1) > 0.2:
      player4_pos.y += 300 * dt

  pygame.display.flip()
  dt = clock.tick(60) / 1000
pygame.quit()
