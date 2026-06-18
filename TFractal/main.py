import numpy as np
from PIL import Image
from colorsys import hsv_to_rgb
from typing import Tuple


class TFractal:
    def __init__(self, seed: np.ndarray, tile_size: int = 5) -> None:
        self.seed = seed
        self.field = None
        self.max_iter = None
        self.tile_size = tile_size
        self.cmap = None
        
    def process(self, iter: int) -> None:
        width, height = self.seed.shape
        step = 2 ** iter
        
        for dx in range(2 ** (self.max_iter - iter)):
            for dy in range(2 ** (self.max_iter - iter)):
                for x in range(width):
                    for y in range(height):
                        if self.seed[x, y]:
                            block = np.ones((step, step))
                        else:
                            block = np.zeros((step, step))

                        self.field[(x + dx * width) * step: (x + dx * width + 1) * step:, 
                                   (y + dy * height) * step: (y + dy * height + 1) * step:] = block
                
        if iter:
            self.process(iter - 1)
        
    def run(self, n_iter: int) -> None:
        self.max_iter = n_iter
        self.field = np.zeros(np.array(self.seed.shape) * (2 ** n_iter))
        self.process(n_iter)
        
    def create_cmap(self, max_val: int) -> None:
        self.cmap = [
            self.get_color(i / max_val) for i in range(int(max_val) + 1)
        ]

    def get_color(self, factor: float) -> Tuple[int, int, int]:
        fact = factor
        if fact < 0: fact = 0
        elif fact > 1: fact = 1

        if fact > 0:
            fact = 1

        start = np.array([0 / 360, 0, 0.0])
        end = np.array([275 / 360, 1, 0.9])

        color = start + fact * (end - start)
        r, g, b = hsv_to_rgb(*color)
        return int(255 * r), int(255 * g), int(255 * b)
        
    def save(self, path: str) -> None:
        step = self.tile_size
        width, height = np.array(self.field.shape)
        max_val = np.max(self.field)
        
        self.create_cmap(max_val)
        
        image = Image.new("RGB", (width * step, height * step), "black")

        for x in range(width):
            for y in range(height):
                for dx in range(step):
                    for dy in range(step):
                        image.putpixel((x * step + dx, y * step + dy), self.cmap[int(self.field[x, y])])

        image.save(path)
        
        
if __name__ == '__main__':

    alient = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], 
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  
        [0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0], 
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0], 
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0], 
        [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]).T

    seed = np.zeros((13 * 3, 10 * 3))
    seed[13:26, 10:20] = alient

    app = TFractal(seed=seed)
    app.run(n_iter=2)

    app.save(f'image.png')
    