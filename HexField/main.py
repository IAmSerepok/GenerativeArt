import numpy as np

from PIL import Image, ImageDraw
from colorsys import hls_to_rgb
from random import randint, seed


class App:
    def __init__(self, field_size, tile_size):
        self.size = field_size
        self.tile_size = tile_size
        self.screen_width, self.screen_height = (3 * tile_size * field_size + self.tile_size, 
                                                 2 * tile_size * field_size + self.tile_size)
        
        self.image = Image.new('RGB', (self.screen_width, self.screen_height), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        
        self.color = self.get_random_color()
        
    @staticmethod
    def get_random_color(rng=None):
        if rng is not None:
            seed(rng)
        h, l, s = randint(0, 360), 0.6, 0.7
        r, g, b = hls_to_rgb(h / 360, l, s)
        return int(255 * r), int(255 * g), int(255 * b)
    
    def draw_hex(self, x, y):
        
        dx = self.tile_size + self.tile_size
        dy = self.tile_size * self.size - self.tile_size / 2
        l = self.tile_size
        
        self.draw.polygon([
                (3 * (x + y) * l / 2 - l + dx, (y - x) * l + dy), 
                (3 * (x + y) * l / 2 - l / 2 + dx, (y - x + 1) * l + dy), 
                (3 * (x + y) * l / 2 + l / 2 + dx, (y - x + 1) * l + dy),
                (3 * (x + y) * l / 2 + l + dx, (y - x) * l + dy),   
                (3 * (x + y) * l / 2 + l / 2 + dx, (y - x - 1) * l + dy),
                (3 * (x + y) * l / 2 - l / 2 + dx, (y - x - 1) * l + dy)
            ], fill=self.get_random_color(), outline='white', width=2)
        
    def run(self):
        for i in range(self.size):
            a, b = i - self.size // 2, i + self.size // 2
            for j in range(self.size):
                x, y = a + j, b - j
                self.draw_hex(x, y)
                
        for i in range(self.size - 1):
            a, b = i - (self.size) // 2 + 1, i + self.size // 2
            for j in range(self.size - 1):
                x, y = a + j, b - j
                self.draw_hex(x, y) 
        
        self.image.show()
        self.image.save('image.png')
        
        
if __name__ == '__main__':
    app = App(10, 20)
    app.run()
