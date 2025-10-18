import pyautogui
import time
import random
import math
import threading

class AutonomousCursor:
    def __init__(self, inactivity_threshold=10):
        self.inactivity_threshold = inactivity_threshold  # секунды бездействия
        self.last_mouse_position = pyautogui.position()
        self.last_activity_time = time.time()
        self.is_active = False
        self.monitor_thread = None
        self.stop_monitoring = False
        
    def start_monitoring(self):
        """Запускает мониторинг активности мыши"""
        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._monitor_activity)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        """Останавливает мониторинг"""
        self.stop_monitoring = True
        self.is_active = False
    
    def _monitor_activity(self):
        """Мониторит активность мыши и запускает автономное поведение при бездействии"""
        while not self.stop_monitoring:
            current_position = pyautogui.position()
            current_time = time.time()
            
            # Проверяем, двигалась ли мышь
            if current_position != self.last_mouse_position:
                self.last_activity_time = current_time
                self.last_mouse_position = current_position
                self.is_active = False
            else:
                # Если мышь не двигалась дольше порога - активируем автономный режим
                if current_time - self.last_activity_time > self.inactivity_threshold and not self.is_active:
                    self.is_active = True
                    self._start_autonomous_behavior()
            
            time.sleep(0.5)  # Проверяем каждые 0.5 секунды
    
    def _start_autonomous_behavior(self):
        """Запускает автономное поведение курсора в отдельном потоке"""
        behavior_thread = threading.Thread(target=self._autonomous_behavior)
        behavior_thread.daemon = True
        behavior_thread.start()
    
    def _autonomous_behavior(self):
        """Таинственное автономное поведение курсора"""
        print("Курсор ожил... кто-то другой взял управление!")
        
        # Получаем текущую позицию
        start_x, start_y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        
        # Случайное количество движений
        num_movements = random.randint(5, 15)
        
        for i in range(num_movements):
            if not self.is_active:  # Прерываем, если пользователь снова начал двигать мышь
                break
                
            # Выбираем тип движения
            movement_type = random.choice(["circle", "figure8", "random", "spiral", "shake"])
            
            if movement_type == "circle":
                self._draw_circle(start_x, start_y, random.randint(30, 100))
            elif movement_type == "figure8":
                self._draw_figure8(start_x, start_y, random.randint(40, 120))
            elif movement_type == "random":
                self._random_movement(start_x, start_y, screen_width, screen_height)
            elif movement_type == "spiral":
                self._draw_spiral(start_x, start_y, random.randint(50, 150))
            elif movement_type == "shake":
                self._shake_movement(start_x, start_y)
            
            # Случайная пауза между движениями
            time.sleep(random.uniform(0.5, 2.0))
            
            # Иногда кликаем случайно
            if random.random() < 0.3:
                pyautogui.click()
        
        # Возвращаем курсор примерно в начальную позицию
        if self.is_active:
            pyautogui.moveTo(start_x + random.randint(-20, 20), 
                            start_y + random.randint(-20, 20), 
                            duration=random.uniform(0.5, 1.5))
        
        print("Курсор снова под вашим контролем... или нет?")
        self.is_active = False
    
    def _draw_circle(self, center_x, center_y, radius):
        """Рисует круг вокруг указанной точки"""
        for angle in range(0, 360, 10):
            if not self.is_active:
                break
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            pyautogui.moveTo(x, y, duration=0.05)
    
    def _draw_figure8(self, center_x, center_y, size):
        """Рисует восьмерку"""
        for t in range(0, 628, 10):  # 0 до 2π с шагом
            if not self.is_active:
                break
            t_rad = t / 100
            x = center_x + size * math.sin(t_rad)
            y = center_y + size * math.sin(t_rad) * math.cos(t_rad)
            pyautogui.moveTo(x, y, duration=0.03)
    
    def _random_movement(self, start_x, start_y, screen_width, screen_height):
        """Случайное блуждание по экрану"""
        for _ in range(random.randint(10, 30)):
            if not self.is_active:
                break
            x = random.randint(0, screen_width - 1)
            y = random.randint(0, screen_height - 1)
            pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.5))
            time.sleep(0.1)
    
    def _draw_spiral(self, center_x, center_y, max_radius):
        """Рисует спираль"""
        for angle in range(0, 720, 5):
            if not self.is_active:
                break
            radius = max_radius * (angle / 720)
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            pyautogui.moveTo(x, y, duration=0.03)
    
    def _shake_movement(self, x, y):
        """Дрожание курсора на месте"""
        for _ in range(20):
            if not self.is_active:
                break
            offset_x = x + random.randint(-10, 10)
            offset_y = y + random.randint(-10, 10)
            pyautogui.moveTo(offset_x, offset_y, duration=0.02)

# Использование
def start_mysterious_cursor(inactivity_time=10):
    """
    Запускает таинственное поведение курсора после указанного времени бездействия
    
    Args:
        inactivity_time (int): время в секундах до активации автономного режима
    """
    cursor = AutonomousCursor(inactivity_threshold=inactivity_time)
    cursor.start_monitoring()
    print(f"Мониторинг запущен. Курсор начнет жить своей жизнью через {inactivity_time} секунд бездействия.")
    print("Нажмите Ctrl+C для остановки.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cursor.stop()
        print("Мониторинг остановлен.")

# Запуск функции
if __name__ == "__main__":
    start_mysterious_cursor(1)  # 10 секунд бездействия
