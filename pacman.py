from globals import Direction, LEVEL_HEIGHT, LEVEL_WIDTH
import events

class Pacman:

    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def move(self, direction):
        if direction == Direction.RIGHT:
            self.x += 1
            if self.x >= LEVEL_WIDTH:
                self.x = 0
        elif direction == Direction.UP:
            self.y -= 1
            if self.y < 0:
                self.y = LEVEL_HEIGHT - 1
        elif direction == Direction.LEFT:
            self.x -= 1
            if self.x < 0:
                self.x = LEVEL_WIDTH - 1
        elif direction == Direction.DOWN:
            self.y += 1
            if self.y >= LEVEL_HEIGHT:
                self.y = 0
        else:
            raise ValueError("Invalid movement direction!")
        
        events.invoke(events.LEVEL_UPDATE)
