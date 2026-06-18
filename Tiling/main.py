from PIL import Image, ImageDraw
import numpy as np


class PlaneTiling:
    def __init__(self, width=800, height=600, background_color=(0, 0, 0)):
        """
        Инициализация холста для замощения
        
        Args:
            width: ширина изображения
            height: высота изображения
            background_color: цвет фона (RGB)
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.image = Image.new('RGB', (width, height), background_color)
        self.draw = ImageDraw.Draw(self.image)
    
    def draw_polygon(self, O, d, color=(255, 255, 255), line_width=2):
        """
        Рисует один полигон заданной формы
        
        Args:
            O: кортеж (x, y) - центр полигона
            d: размер полигона
            color: цвет линий
            line_width: толщина линий
        """
        O_x, O_y = O
        sqrt2_d = np.sqrt(2) * d
        sqrt2_2_d = np.sqrt(2) / 2 * d
        
        points = [
            (O_x, O_y + 2 * d),                           # (O.x, O.y + 2d)
            (O_x + sqrt2_2_d, O_y + 1.5 * d),             # (O.x + √2/2 d, O.y + 3/2 d)
            (O_x + sqrt2_2_d, O_y + 0.5 * d),             # (O.x + √2/2 d, O.y + 1/2 d)
            (O_x + sqrt2_d, O_y),                         # (O.x + √2 d, O.y)
            (O_x + sqrt2_d, O_y - d),                     # (O.x + √2 d, O.y - d)
            (O_x + sqrt2_2_d, O_y - 1.5 * d),             # (O.x + √2/2 d, O.y - 3/2 d)
            (O_x, O_y - d),                               # (O.x, O.y - d)
            (O_x - sqrt2_2_d, O_y - 1.5 * d),             # (O.x - √2/2 d, O.y - 3/2 d)
            (O_x - sqrt2_d, O_y - d),                     # (O.x - √2 d, O.y - d)
            (O_x - sqrt2_d, O_y),                         # (O.x - √2 d, O.y)
            (O_x - sqrt2_2_d, O_y + 0.5 * d),             # (O.x - √2/2 d, O.y + 1/2 d)
            (O_x - sqrt2_2_d, O_y + 1.5 * d),             # (O.x - √2/2 d, O.y + 3/2 d)
            (O_x, O_y + 2 * d)                            # Замыкаем полигон
        ]
        
        # Рисуем полигон
        self.draw.polygon(points, outline=color, width=line_width)
    
    def draw_pattern(self, d=30, color=(255, 255, 255), repeat=2, line_width=2):
        """
        Замощение плоскости полигонами по заданному алгоритму
        
        Args:
            d: размер полигона
            color: цвет линий
            line_width: толщина линий
        """
        sqrt2 = np.sqrt(2)
        
        # Первый цикл отрисовки - начинаем с точки A1
        A1_x = -3 * d
        A1_y = -6 * d
        
        self._draw_pattern_grid(A1_x, A1_y, d, color, repeat, line_width)
        
        # Второй цикл отрисовки - начинаем со смещенной точки
        A2_x = A1_x + (3 * sqrt2 / 2) * d
        A2_y = A1_y + (3 / 2) * d
        
        self._draw_pattern_grid(A2_x, A2_y, d, color, repeat, line_width)
    
    def _draw_pattern_grid(self, start_x, start_y, d, color, repeat, line_width):
        """
        Вспомогательная функция для отрисовки сетки полигонов
        
        Args:
            start_x: начальная координата X
            start_y: начальная координата Y
            d: размер полигона
            color: цвет линий
            repeat: количество вложений
            line_width: толщина линий
        """
        sqrt2 = np.sqrt(2)
        
        # Шаг по вертикали
        vertical_step = 3 * d
        # Шаг по горизонтали
        horizontal_step = 3 * sqrt2 * d
        
        x = start_x
        y = start_y
        
        # Флаг для определения, нужно ли продолжать рисование
        continue_drawing = True
        column_count = 0
        
        while continue_drawing:
            row_has_polygons = False
            polygons_in_column = 0

            current_y = y
            while current_y < self.height + 3 * d:
                if (x + 3 * sqrt2 * d > 0 and x - 3 * sqrt2 * d < self.width and
                    current_y + 3 * d > 0 and current_y - 3 * d < self.height):
                    
                    for d in np.linspace(0, d, repeat)[1:]:
                        self.draw_polygon((x, current_y), d, color, line_width)

                    row_has_polygons = True
                    polygons_in_column += 1
                
                current_y += vertical_step
            
            # Если в этом столбце были полигоны, переходим к следующему столбцу
            if row_has_polygons:
                x += horizontal_step
                column_count += 1
            else:
                # Если в столбце не было полигонов, значит вышли за границы холста
                continue_drawing = False
    
    def save_tiling(self, filename):
        """
        Сохранение замощения в файл
        
        Args:
            filename: имя файла
        """
        
        self.image.save(filename)
        print(f"Замощение сохранено как {filename}")
    
    def show_tiling(self):
        """Показать изображение"""
        self.image.show()


if __name__ == "__main__":
    tiling = PlaneTiling(width=1600, height=900, background_color=(0, 0, 0))

    tiling.draw_pattern(d=100, color=(255, 255, 255), repeat=2, line_width=3)

    tiling.save_tiling("output/tiling_pattern.png")
    tiling.show_tiling()
