import py5
import numpy as np
from scipy.interpolate import CubicSpline
from random import uniform, randint

def setup():
    py5.size(1000, 700)
    py5.background(0)
    draw_lines()

def draw_lines():
    t = np.linspace(0, 1, 20)
    
    for y0 in range(3):
        # Масштабируем y0 к координатам экрана
        screen_y0 = py5.remap(y0, 0, 2, 50, py5.height-50)
        
        # Генерируем основную линию
        y = uniform(-0.3, 0.3) * t + np.random.uniform(-0.05, 0.05, len(t))
        y = [screen_y0 + yi * 100 for yi in y]  # Масштабируем амплитуду
        
        # Основная линия (сплайн)
        cs = CubicSpline(t, y, bc_type='natural')
        new_t = np.linspace(0, 1, 500)
        new_y = cs(new_t)
        
        # Рисуем основную линию
        py5.stroke(255)
        py5.stroke_weight(3)
        py5.no_fill()
        py5.begin_shape()
        for x, y_val in zip(new_t, new_y):
            py5.vertex(x * py5.width, y_val)
        py5.end_shape()
        
        # Текстура (песочный эффект)
        for _ in range(30):
            noise = np.random.uniform(-5, 5, len(t))
            noisy_y = y + noise
            
            cs_noise = CubicSpline(t, noisy_y, bc_type='natural')
            detail = randint(500, 2000)
            new_t_noise = np.linspace(0, 1, detail)
            new_y_noise = cs_noise(new_t_noise)
            
            # Рисуем точки текстуры
            py5.stroke(255, 170)  
            py5.stroke_weight(0.7)
            for x, y_val in zip(new_t_noise, new_y_noise):
                py5.point(x * py5.width, y_val)

def key_pressed():
    py5.background(0)
    draw_lines()

py5.run_sketch()