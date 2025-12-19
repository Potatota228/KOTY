import pygame as pg
import sys
from config import WIDTH, HEIGHT, FPS
from resource_manager import ResourceManager

class Director:
    """Главный контроллер игры"""
    
    def __init__(self):
        pg.init()
        pg.mixer.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("KOTY")
        
        self.clock = pg.time.Clock()
        self.running = True
        
        # Менеджер ресурсов с загрузкой из конфига
        self.resource_manager = ResourceManager("resources.json")
        self.resource_manager.preload_all_resources()
        
        # Словарь сцен (загружаем после инициализации ресурсов)
        self.scenes = {}
        self._register_scenes()
        
        self.current_scene = None
        self.switch_scene("menu")
    
    def _register_scenes(self):
        """Регистрация всех сцен игры"""
        from Scenes import MenuScene, CreationScene, InfoBoxScene
        
        self.scenes = {
            "menu": MenuScene(self),
            "creation": CreationScene(self),
            "infobox": InfoBoxScene(self)
        }
        
        # Можно добавить дополнительные сцены для демонстрации
        # from Scenes.sceneExample import ExampleScene
        # self.scenes["example"] = ExampleScene(self)
    
    def switch_scene(self, scene_name, **kwargs):
        """
        Переключение между сценами
        
        Args:
            scene_name: имя сцены
            **kwargs: дополнительные параметры для передачи в сцену
        """
        if scene_name not in self.scenes:
            print(f"⚠ Сцена '{scene_name}' не найдена!")
            return
        
        # Вызываем on_exit у текущей сцены
        if self.current_scene:
            self.current_scene.on_exit()
        
        # Переключаем сцену
        self.current_scene = self.scenes[scene_name]
        
        # Передаём параметры в сцену если они есть
        if kwargs:
            for key, value in kwargs.items():
                setattr(self.current_scene, key, value)
        
        # Вызываем on_enter у новой сцены
        self.current_scene.on_enter()
        
        print(f"→ Переход на сцену: {scene_name}")
    
    def quit(self):
        """Завершение работы"""
        self.running = False
    
    def run(self):
        """Главный игровой цикл"""
        print("\n=== Запуск игры ===\n")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
            
            # Обработка событий, обновление и отрисовка
            self.current_scene.handle_events(events)
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)
            
            pg.display.flip()
        
        # Очистка ресурсов
        print("\n=== Завершение работы ===")
        self.resource_manager.clear()
        pg.quit()
        sys.exit()