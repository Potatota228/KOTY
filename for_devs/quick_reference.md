# 🚀 Шпаргалка: Pygame + UI System

## 📦 Основы pygame

### Инициализация
```python
import pygame as pg
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
```

### Главный цикл
```python
running = True
while running:
    dt = clock.tick(60) / 1000  # 60 FPS, dt в секундах
    
    # 1. События
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # 2. Обновление
    # ... логика игры
    
    # 3. Отрисовка
    screen.fill((255, 255, 255))  # Белый фон
    # ... рисуем объекты
    pg.display.flip()
```

### Работа с изображениями
```python
# Загрузка
image = pg.image.load("image.png").convert_alpha()

# Масштабирование
image = pg.transform.scale(image, (100, 100))

# Отрисовка
screen.blit(image, (x, y))  # (x, y) — верхний левый угол

# Rect для позиционирования
rect = image.get_rect()
rect.center = (400, 300)      # По центру
rect.topleft = (0, 0)         # Левый верхний угол
rect.bottom = 600             # Прижать к низу
screen.blit(image, rect)
```

### События
```python
# Типы событий
pg.QUIT                # Закрытие окна
pg.KEYDOWN             # Нажатие клавиши
pg.KEYUP               # Отпускание клавиши
pg.MOUSEBUTTONDOWN     # Клик мыши
pg.MOUSEBUTTONUP       # Отпускание кнопки мыши
pg.MOUSEMOTION         # Движение мыши

# Проверка клавиш
if event.type == pg.KEYDOWN:
    if event.key == pg.K_SPACE:    # Пробел
        print("Space pressed")
    if event.key == pg.K_ESCAPE:   # ESC
        print("Escape pressed")
    if event.key == pg.K_RETURN:   # Enter
        print("Enter pressed")

# Проверка мыши
if event.type == pg.MOUSEBUTTONDOWN:
    if event.button == 1:          # ЛКМ
        print(f"Клик в {event.pos}")
    if event.button == 3:          # ПКМ
        print("Правая кнопка")

# Позиция мыши
mouse_pos = pg.mouse.get_pos()
mouse_buttons = pg.mouse.get_pressed()  # (left, middle, right)
```

### Текст
```python
# Создание шрифта
font = pg.font.Font("font.ttf", 24)
font = pg.font.Font(None, 24)  # Системный шрифт

# Рендер текста
text_surf = font.render("Hello", True, (0, 0, 0))  # Чёрный
text_rect = text_surf.get_rect(center=(400, 300))
screen.blit(text_surf, text_rect)
```

### Звук
```python
# Загрузка
sound = pg.mixer.Sound("sound.wav")
sound.set_volume(0.5)  # 0.0 - 1.0

# Воспроизведение
sound.play()

# Фоновая музыка
pg.mixer.music.load("music.mp3")
pg.mixer.music.play(-1)  # -1 = зациклить
pg.mixer.music.stop()
```

---

## 🎨 Новая система UI

### Создание сцены
```python
from Scenes.scene import Scene

class MyScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self._setup_ui()
    
    def _setup_ui(self):
        """Создаём UI элементы"""
        # Ваш код
    
    def on_enter(self):
        """Вызывается при входе"""
        self.show_group("main")
    
    def on_exit(self):
        """Вызывается при выходе"""
        pass
    
    def handle_events(self, events):
        super().handle_events(events)  # ВАЖНО!
    
    def update(self, dt):
        super().update(dt)  # ВАЖНО!
    
    def render(self, screen):
        screen.fill((255, 255, 255))
        super().render(screen)  # В КОНЦЕ!
```

### Работа с UI элементами
```python
# Создание
button = Button(x, y, image, scale, "Text", font)
text = Text(x, y, "Hello", font)
input_box = Input_box(image, x, y, font)

# Добавление в менеджер
self.add_ui(button, group="menu")

# Группы
self.show_group("menu")      # Показать
self.hide_group("menu")      # Скрыть
self.ui_manager.disable_group("menu")  # Деактивировать
self.ui_manager.enable_group("menu")   # Активировать

# Callbacks
button.on_click = lambda btn: print("Clicked!")
input_box.on_submit = lambda inp, text: print(f"Entered: {text}")
input_box.on_text_change = lambda inp, text: self.validate(text)

# Состояния
button.enabled = False   # Деактивировать
button.visible = False   # Скрыть
button.focus()          # Установить фокус
```

### ResourceManager
```python
# Получение ресурсов
image = self.resource_manager.get_image("button")
font = self.resource_manager.get_font("main", 20)
sound = self.resource_manager.get_sound("click")

# Все ресурсы определены в resources.json
```

### Director (переключение сцен)
```python
# Переход на другую сцену
self.director.switch_scene("menu")

# С передачей параметров
self.director.switch_scene("game", player_name="Hero", level=1)

# Выход из игры
self.director.quit()
```

---

## 💡 Частые паттерны

### Центрирование
```python
# По центру экрана (800x600)
element.rect.center = (400, 300)

# По центру другого элемента
text_rect.center = button_rect.center
```

### Проверка столкновений
```python
# Точка внутри прямоугольника
if rect.collidepoint(mouse_pos):
    print("Мышь на объекте")

# Прямоугольник пересекается с другим
if rect1.colliderect(rect2):
    print("Столкновение!")
```

### Анимация с dt
```python
# Движение
speed = 100  # пикселей в секунду
position += speed * dt

# Плавное изменение
target = 255
current += (target - current) * 5 * dt
```

### Условная отрисовка
```python
if button.visible and button.enabled:
    button.draw(screen)
```

---

## 🐛 Отладка

### Вывод в консоль
```python
print(f"Position: {x}, {y}")
print(f"Button clicked: {button.clicked}")
```

### Рисование отладочных прямоугольников
```python
# Красный прямоугольник вокруг объекта
pg.draw.rect(screen, (255, 0, 0), rect, 2)  # 2 = толщина рамки
```

### Проверка FPS
```python
fps = clock.get_fps()
print(f"FPS: {fps:.2f}")
```

---

## 📝 Цвета (RGB)
```python
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# С прозрачностью (RGBA) - для Surface
color = (255, 0, 0, 128)  # Полупрозрачный красный
```

---

## ⚡ Оптимизация

### Что НЕ делать
```python
# ❌ Создавать объекты каждый кадр
def render(self):
    button = Button(...)  # МЕДЛЕННО!
    
# ❌ Загружать изображения каждый кадр
def render(self):
    image = pg.image.load("img.png")  # ОЧЕНЬ МЕДЛЕННО!
```

### Что делать
```python
# ✅ Создавать один раз
def __init__(self):
    self.button = Button(...)
    self.image = pg.image.load("img.png")

def render(self):
    self.button.draw(screen)
```

---

## 🔗 Полезные методы Rect

```python
rect = pg.Rect(x, y, width, height)

# Позиции углов
rect.topleft = (x, y)
rect.topright = (x, y)
rect.bottomleft = (x, y)
rect.bottomright = (x, y)

# Центры сторон
rect.midtop = (x, y)
rect.midbottom = (x, y)
rect.midleft = (x, y)
rect.midright = (x, y)

# Центр
rect.center = (x, y)
rect.centerx = x
rect.centery = y

# Размеры
rect.width = 100
rect.height = 50
rect.size = (100, 50)

# Границы
rect.left, rect.right
rect.top, rect.bottom

# Методы
rect.move(dx, dy)          # Вернуть новый Rect
rect.move_ip(dx, dy)       # Изменить на месте (in place)
rect.inflate(dx, dy)       # Увеличить размер
rect.clamp(other_rect)     # Вместить в другой Rect
```

---

## 📚 Ресурсы

- **Документация**: https://www.pygame.org/docs/
- **Примеры**: в папке `examples/` вашего проекта
- **Справка по коду**: читайте docstrings — `help(Button)`