import numpy as np
from PIL import Image
from typing import Tuple, Optional


class TFractal:
    def __init__(self, seed_image: Image.Image, tile_size: int = 5) -> None:
        """
        Инициализация с RGBA изображением-семенем
        
        Args:
            seed_image: PIL Image в режиме RGBA
            tile_size: размер тайла для отрисовки
        """
        self.seed = np.array(seed_image)
        self.field = None
        self.max_iter = None
        self.tile_size = tile_size
        self.scale_factor = 2  # Во сколько раз увеличивается изображение на каждой итерации
        
    def process(self, iter: int) -> None:
        """Рекурсивно вкладывает изображение-семя"""
        seed_height, seed_width = self.seed.shape[:2]
        step = self.scale_factor ** iter
        
        # Размер текущего блока семени в поле
        block_size = step
        
        for dx in range(self.scale_factor ** (self.max_iter - iter)):
            for dy in range(self.scale_factor ** (self.max_iter - iter)):
                for x in range(seed_height):
                    for y in range(seed_width):
                        # Берем пиксель из семени
                        pixel = self.seed[x, y]
                        
                        # Заполняем блок соответствующим пикселем
                        x_start = (x + dx * seed_height) * block_size
                        y_start = (y + dy * seed_width) * block_size
                        
                        for bx in range(block_size):
                            for by in range(block_size):
                                if x_start + bx < self.field.shape[0] and y_start + by < self.field.shape[1]:
                                    self.field[x_start + bx, y_start + by] = pixel
                
        if iter:
            self.process(iter - 1)
        
    def run(self, n_iter: int) -> None:
        """
        Запускает процесс создания фрактала
        
        Args:
            n_iter: количество итераций
        """
        self.max_iter = n_iter
        seed_height, seed_width = self.seed.shape[:2]
        
        # Рассчитываем итоговый размер с учетом scale_factor
        final_height = seed_height * (self.scale_factor ** n_iter)
        final_width = seed_width * (self.scale_factor ** n_iter)
        
        # Создаем поле RGBA
        self.field = np.zeros((final_height, final_width, 4), dtype=np.uint8)
        self.process(n_iter)
        
    def blend_with_background(self, background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> None:
        """
        Смешивает RGBA изображение с фоном
        
        Args:
            background_color: цвет фона в формате RGBA
        """
        if self.field is None:
            raise ValueError("Сначала запустите run()")
            
        bg_array = np.full(self.field.shape, background_color, dtype=np.uint8)
        
        # Нормализуем альфа-канал
        alpha = self.field[:, :, 3:4].astype(np.float32) / 255.0
        
        # Смешиваем цвета
        self.field = (self.field[:, :, :3] * alpha + 
                      bg_array[:, :, :3] * (1 - alpha)).astype(np.uint8)
        
    def save(self, path: str, blend_background: bool = False, 
             background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> None:
        """
        Сохраняет изображение
        
        Args:
            path: путь для сохранения
            blend_background: нужно ли смешивать с фоном
            background_color: цвет фона если blend_background=True
        """
        if self.field is None:
            raise ValueError("Сначала запустите run()")
            
        field_to_save = self.field.copy()
        
        if blend_background:
            self.blend_with_background(background_color)
        
        # Создаем увеличенное изображение с тайлами
        height, width = field_to_save.shape[:2]
        output_height = height * self.tile_size
        output_width = width * self.tile_size
        
        if blend_background:
            image = Image.new("RGB", (output_width, output_height), tuple(background_color[:3]))
            mode = "RGB"
        else:
            image = Image.new("RGBA", (output_width, output_height), (0, 0, 0, 0))
            mode = "RGBA"
        
        for x in range(height):
            for y in range(width):
                pixel = tuple(field_to_save[x, y])
                for dx in range(self.tile_size):
                    for dy in range(self.tile_size):
                        image.putpixel((y * self.tile_size + dy, x * self.tile_size + dx), pixel)
        
        image.save(path)


# Пример использования
def create_fractal_from_image():
    # Загружаем произвольное RGBA изображение
    seed_image = Image.open("your_image.png").convert("RGBA")
    
    # Создаем фрактал
    fractal = TFractal(seed_image, tile_size=3)
    fractal.run(n_iter=3)  # 3 итерации
    
    # Сохраняем с прозрачностью
    fractal.save("fractal_transparent.png", blend_background=False)
    
    # Сохраняем с белым фоном
    fractal.save("fractal_on_white.png", blend_background=True, background_color=(255, 255, 255, 255))
    
    # Сохраняем с черным фоном
    fractal.save("fractal_on_black.png", blend_background=True, background_color=(0, 0, 0, 255))


# Упрощенная версия без увеличения пикселей (для быстрой визуализации)
class FastTFractal(TFractal):
    def save(self, path: str, blend_background: bool = False, 
             background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)) -> None:
        """Быстрое сохранение без увеличения пикселей"""
        if self.field is None:
            raise ValueError("Сначала запустите run()")
            
        field_to_save = self.field.copy()
        
        if blend_background:
            self.blend_with_background(background_color)
            image = Image.fromarray(field_to_save[:, :, :3], 'RGB')
        else:
            image = Image.fromarray(field_to_save, 'RGBA')
        
        image.save(path)


if __name__ == "__main__":
    img = Image.open("TFractal/1.png").convert("RGBA")
    fractal = TFractal(img, tile_size=16)
    fractal.run(n_iter=0)
    fractal.save("fractal_output.png")
