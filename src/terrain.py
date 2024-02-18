import sys, time, random, math, pygame

grid_point = 0

class Terrain(pygame.sprite.Sprite):

    def __init__(self, min_height, max_height, total_points):
        # initialisation de la superclass sprite
        super().__init__()
        self.min_height = min_height
        self.max_height = max_height
        self.total_points = total_points+1
        self.grid_size = 1080 / total_points
        self.height_map = list()
        self.generate()


    def generate(self):
        #clear list
        if len(self.height_map)>0:
            for n in range(self.total_points):
                self.height_map.pop()

        #first point
        last_x = 0
        last_height = (self.max_height + self.min_height) / 2
        self.height_map.append( last_height )
        direction = 1
        run_length = 0

        #remaining points
        for n in range( 1, self.total_points ):
            rand_dist = random.randint(1, 10) * direction
            height = last_height + rand_dist
            self.height_map.append( int(height) )
            if height < self.min_height: direction = -1
            elif height > self.max_height: direction = 1
            last_height = height
            if run_length <= 0:
                run_length = random.randint(1,3)
                direction = random.randint(1,2)
                if direction == 2: direction = -1
            else:
                run_length -= 1

    def get_height(self,x):
        x_point = int(x / self.grid_size)
        return self.height_map[x_point]

    def draw(self, surface):
        global player_firing
        last_x = 0
        for n in range( 1, self.total_points ):
            #draw circle at current point
            height = 600 - self.height_map[n]
            x_pos = int(n * self.grid_size)
            pos = (x_pos, height)
            color = (255,255,255)
            #pygame.draw.circle(surface, color, pos, 4, 1)
            if n == grid_point:
                pygame.draw.circle(surface, (0,255,0), pos, 4, 0)
            #draw line from previous point
            last_height = 600 - self.height_map[n-1]
            last_pos = (last_x, last_height)
            pygame.draw.line(surface, color, last_pos, pos, 2)
            last_x = x_pos