import time
import os
import sys

class ConsoleTrafficLight:
    def __init__(self):
        # Тайминги светофора (в секундах)
        self.RED_TIME = 5
        self.YELLOW_TIME = 2
        self.GREEN_TIME = 5
        
        # Состояния светофора
        self.STATES = ["RED", "RED_YELLOW", "GREEN", "YELLOW"]
        self.current_state = "RED"
        self.state_start_time = time.time()
        
        # Цвета для терминала (ANSI коды)
        self.COLORS = {
            "RED": "\033[91m",      # Красный
            "YELLOW": "\033[93m",   # Желтый
            "GREEN": "\033[92m",    # Зеленый
            "ORANGE": "\033[38;5;214m",  # Оранжевый
            "RESET": "\033[0m",     # Сброс цвета
            "BOLD": "\033[1m"       # Жирный
        }
        
        # Символы для светофора
        self.LIGHT_SYMBOLS = {
            "RED_ON": "🔴",
            "RED_OFF": "⚫",
            "YELLOW_ON": "🟡",
            "YELLOW_OFF": "⚫",
            "GREEN_ON": "🟢",
            "GREEN_OFF": "⚫"
        }
        
    def clear_screen(self):
        """Очистка экрана терминала"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_traffic_light(self):
        """Отображение светофора в терминале"""
        self.clear_screen()
        
        # Заголовок
        print(f"{self.COLORS['BOLD']}{'='*40}{self.COLORS['RESET']}")
        print(f"{self.COLORS['BOLD']}   🚦 ВИРТУАЛЬНЫЙ СВЕТОФОР 🚦   {self.COLORS['RESET']}")
        print(f"{self.COLORS['BOLD']}{'='*40}{self.COLORS['RESET']}")
        print()
        
        # Определяем какие лампы горят
        if self.current_state == "RED":
            red_light = self.LIGHT_SYMBOLS["RED_ON"]
            yellow_light = self.LIGHT_SYMBOLS["YELLOW_OFF"]
            green_light = self.LIGHT_SYMBOLS["GREEN_OFF"]
            color = self.COLORS["RED"]
            text = "🔴 СТОЙ!"
            
        elif self.current_state == "RED_YELLOW":
            red_light = self.LIGHT_SYMBOLS["RED_ON"]
            yellow_light = self.LIGHT_SYMBOLS["YELLOW_ON"]
            green_light = self.LIGHT_SYMBOLS["GREEN_OFF"]
            color = self.COLORS["ORANGE"]
            text = "🟠 ПРИГОТОВЬТЕСЬ!"
            
        elif self.current_state == "GREEN":
            red_light = self.LIGHT_SYMBOLS["RED_OFF"]
            yellow_light = self.LIGHT_SYMBOLS["YELLOW_OFF"]
            green_light = self.LIGHT_SYMBOLS["GREEN_ON"]
            color = self.COLORS["GREEN"]
            text = "🟢 ИДИТЕ!"
            
        elif self.current_state == "YELLOW":
            red_light = self.LIGHT_SYMBOLS["RED_OFF"]
            yellow_light = self.LIGHT_SYMBOLS["YELLOW_ON"]
            green_light = self.LIGHT_SYMBOLS["GREEN_OFF"]
            color = self.COLORS["YELLOW"]
            text = "🟡 ВНИМАНИЕ!"
        
        # Рисуем светофор
        print(f"{' ' * 15}╔═══════╗")
        print(f"{' ' * 15}║       ║")
        print(f"{' ' * 15}║   {red_light}   ║")
        print(f"{' ' * 15}║       ║")
        print(f"{' ' * 15}║   {yellow_light}   ║")
        print(f"{' ' * 15}║       ║")
        print(f"{' ' * 15}║   {green_light}   ║")
        print(f"{' ' * 15}║       ║")
        print(f"{' ' * 15}╚═══════╝")
        print()
        
        # Текущее состояние
        print(f"{color}{' ' * 10}{text}{self.COLORS['RESET']}")
        print()
        
        # Время до следующего переключения
        current_time = time.time()
        elapsed_time = current_time - self.state_start_time
        
        if self.current_state == "RED":
            time_left = self.RED_TIME - elapsed_time
        elif self.current_state == "RED_YELLOW" or self.current_state == "YELLOW":
            time_left = self.YELLOW_TIME - elapsed_time
        elif self.current_state == "GREEN":
            time_left = self.GREEN_TIME - elapsed_time
        
        if time_left > 0:
            print(f"⏱️  До смены: {time_left:.1f} сек.")
        else:
            print(f"⏱️  Смена сейчас!")
        
        print()
        print(f"{self.COLORS['BOLD']}Состояние: {self.current_state}{self.COLORS['RESET']}")
        print(f"{self.COLORS['BOLD']}{'='*40}{self.COLORS['RESET']}")
        
        # Инструкции
        print("\nУправление:")
        print("  R - Красный свет")
        print("  Y - Желтый свет") 
        print("  G - Зеленый свет")
        print("  A - Автоматический режим")
        print("  B - Мигающий желтый (аварийный)")
        print("  Q - Выход")
    
    def set_lights(self, state):
        """Установка состояния светофора"""
        self.current_state = state
        self.state_start_time = time.time()
        self.display_traffic_light()
    
    def switch_state(self):
        """Автоматическое переключение состояния"""
        if self.current_state == "RED":
            self.set_lights("RED_YELLOW")
            print("🔄 Переключаюсь на КРАСНЫЙ+ЖЕЛТЫЙ")
            
        elif self.current_state == "RED_YELLOW":
            self.set_lights("GREEN")
            print("🔄 Переключаюсь на ЗЕЛЕНЫЙ")
            
        elif self.current_state == "GREEN":
            self.set_lights("YELLOW")
            print("🔄 Переключаюсь на ЖЕЛТЫЙ")
            
        elif self.current_state == "YELLOW":
            self.set_lights("RED")
            print("🔄 Переключаюсь на КРАСНЫЙ")
    
    def check_timeout(self):
        """Проверка таймаута для автоматического переключения"""
        current_time = time.time()
        elapsed_time = current_time - self.state_start_time
        
        if self.current_state == "RED" and elapsed_time >= self.RED_TIME:
            return True
        elif (self.current_state == "RED_YELLOW" or self.current_state == "YELLOW") and elapsed_time >= self.YELLOW_TIME:
            return True
        elif self.current_state == "GREEN" and elapsed_time >= self.GREEN_TIME:
            return True
        
        return False
    
    def emergency_blink(self):
        """Аварийный мигающий режим"""
        if self.blink_mode:
            if self.current_state == "YELLOW":
                # Имитация выключенной лампы
                temp_state = self.current_state
                self.current_state = "OFF"
                self.display_traffic_light()
                time.sleep(0.5)
                self.current_state = temp_state
            else:
                self.set_lights("YELLOW")
    
    def run(self):
        """Главный цикл программы"""
        self.display_traffic_light()
        
        try:
            while self.is_running:
                # Проверяем ввод пользователя
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1).upper()
                    
                    if key == 'R':
                        self.auto_mode = False
                        self.blink_mode = False
                        self.set_lights("RED")
                        print("🎮 Ручное управление: Установлен КРАСНЫЙ")
                        
                    elif key == 'Y':
                        self.auto_mode = False
                        self.blink_mode = False
                        self.set_lights("YELLOW")
                        print("🎮 Ручное управление: Установлен ЖЕЛТЫЙ")
                        
                    elif key == 'G':
                        self.auto_mode = False
                        self.blink_mode = False
                        self.set_lights("GREEN")
                        print("🎮 Ручное управление: Установлен ЗЕЛЕНЫЙ")
                        
                    elif key == 'A':
                        self.auto_mode = not self.auto_mode
                        if self.auto_mode:
                            self.blink_mode = False
                            print("🤖 Автоматический режим ВКЛЮЧЕН")
                        else:
                            print("🖐️ Автоматический режим ВЫКЛЮЧЕН")
                            
                    elif key == 'B':
                        self.blink_mode = not self.blink_mode
                        self.auto_mode = False
                        if self.blink_mode:
                            print("🚨 Аварийный режим ВКЛЮЧЕН")
                        else:
                            print("✅ Аварийный режим ВЫКЛЮЧЕН")
                            
                    elif key == 'Q':
                        print("\n👋 Завершение работы...")
                        self.is_running = False
                        break
                
                # Автоматический режим
                if self.auto_mode and self.check_timeout():
                    self.switch_state()
                
                # Аварийный режим
                if self.blink_mode:
                    self.emergency_blink()
                    time.sleep(0.5)
                else:
                    # Обновляем отображение каждые 0.5 секунды
                    time.sleep(0.5)
                    self.display_traffic_light()
                    
        except KeyboardInterrupt:
            print("\n\n👋 Программа завершена пользователем")
        finally:
            print(f"{self.COLORS['RESET']}")

# Альтернативная версия без select (для Windows)
class SimpleConsoleTrafficLight:
    def __init__(self):
        self.RED_TIME = 5
        self.YELLOW_TIME = 2
        self.GREEN_TIME = 5
        self.current_state = "RED"
        self.state_start_time = time.time()
        self.auto_mode = True
        self.is_running = True
        
    def display(self):
        """Простое отображение без очистки экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 40)
        print("        🚦 ВИРТУАЛЬНЫЙ СВЕТОФОР 🚦")
        print("=" * 40)
        print()
        
        # ASCII арт светофора
        if self.current_state == "RED":
            print("        ╔═══════╗")
            print("        ║  🔴   ║   🔴 СТОЙ!")
            print("        ║  ⚫   ║")
            print("        ║  ⚫   ║")
            print("        ╚═══════╝")
            
        elif self.current_state == "RED_YELLOW":
            print("        ╔═══════╗")
            print("        ║  🔴   ║   🟠 ПРИГОТОВЬТЕСЬ!")
            print("        ║  🟡   ║")
            print("        ║  ⚫   ║")
            print("        ╚═══════╝")
            
        elif self.current_state == "GREEN":
            print("        ╔═══════╗")
            print("        ║  ⚫   ║   🟢 ИДИТЕ!")
            print("        ║  ⚫   ║")
            print("        ║  🟢   ║")
            print("        ╚═══════╝")
            
        elif self.current_state == "YELLOW":
            print("        ╔═══════╗")
            print("        ║  ⚫   ║   🟡 ВНИМАНИЕ!")
            print("        ║  🟡   ║")
            print("        ║  ⚫   ║")
            print("        ╚═══════╝")
        
        print()
        current_time = time.time()
        elapsed_time = current_time - self.state_start_time
        
        # Время до смены
        if self.current_state == "RED":
            time_left = self.RED_TIME - elapsed_time
        elif self.current_state in ["RED_YELLOW", "YELLOW"]:
            time_left = self.YELLOW_TIME - elapsed_time
        elif self.current_state == "GREEN":
            time_left = self.GREEN_TIME - elapsed_time
        
        print(f"Состояние: {self.current_state}")
        print(f"Время до смены: {max(0, time_left):.1f} сек.")
        print()
        print("=" * 40)
        print("\nДля выхода нажмите Ctrl+C")
    
    def run_simple(self):
        """Упрощенный главный цикл"""
        print("Запуск виртуального светофора...")
        print("Нажмите Ctrl+C для выхода")
        print()
        
        try:
            while self.is_running:
                self.display()
                
                # Проверяем время для автоматического переключения
                current_time = time.time()
                elapsed_time = current_time - self.state_start_time
                
                if self.auto_mode:
                    if self.current_state == "RED" and elapsed_time >= self.RED_TIME:
                        self.current_state = "RED_YELLOW"
                        self.state_start_time = current_time
                        print("🔄 Переключаюсь на КРАСНЫЙ+ЖЕЛТЫЙ")
                        
                    elif self.current_state == "RED_YELLOW" and elapsed_time >= self.YELLOW_TIME:
                        self.current_state = "GREEN"
                        self.state_start_time = current_time
                        print("🔄 Переключаюсь на ЗЕЛЕНЫЙ")
                        
                    elif self.current_state == "GREEN" and elapsed_time >= self.GREEN_TIME:
                        self.current_state = "YELLOW"
                        self.state_start_time = current_time
                        print("🔄 Переключаюсь на ЖЕЛТЫЙ")
                        
                    elif self.current_state == "YELLOW" and elapsed_time >= self.YELLOW_TIME:
                        self.current_state = "RED"
                        self.state_start_time = current_time
                        print("🔄 Переключаюсь на КРАСНЫЙ")
                
                # Ждем 0.5 секунды перед обновлением
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n👋 Программа завершена")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

# Самая простая версия (для новичков)
def super_simple_traffic_light():
    """Самый простой светофор в терминале"""
    states = ["🔴 КРАСНЫЙ", "🟠 КРАСНЫЙ+ЖЕЛТЫЙ", "🟢 ЗЕЛЕНЫЙ", "🟡 ЖЕЛТЫЙ"]
    times = [5, 2, 5, 2]  # Время для каждого состояния
    current = 0
    
    print("🚦 Простой виртуальный светофор")
    print("Нажмите Ctrl+C для выхода")
    print()
    
    try:
        while True:
            print("\n" + "="*40)
            print(f"Состояние: {states[current]}")
            
            # Отображаем светофор
            if current == 0:  # RED
                print("     ╔═══════╗")
                print("     ║  🔴   ║   СТОЙ!")
                print("     ║  ⚫   ║")
                print("     ║  ⚫   ║")
                print("     ╚═══════╝")
            elif current == 1:  # RED_YELLOW
                print("     ╔═══════╗")
                print("     ║  🔴   ║   ПРИГОТОВЬТЕСЬ!")
                print("     ║  🟡   ║")
                print("     ║  ⚫   ║")
                print("     ╚═══════╝")
            elif current == 2:  # GREEN
                print("     ╔═══════╗")
                print("     ║  ⚫   ║   ИДИТЕ!")
                print("     ║  ⚫   ║")
                print("     ║  🟢   ║")
                print("     ╚═══════╝")
            elif current == 3:  # YELLOW
                print("     ╔═══════╗")
                print("     ║  ⚫   ║   ВНИМАНИЕ!")
                print("     ║  🟡   ║")
                print("     ║  ⚫   ║")
                print("     ╚═══════╝")
            
            print("="*40)
            
            # Ждем указанное время
            for i in range(times[current], 0, -1):
                print(f"До смены: {i} сек.", end="\r")
                time.sleep(1)
            
            # Переключаем состояние
            current = (current + 1) % len(states)
            
    except KeyboardInterrupt:
        print("\n\n👋 Светофор остановлен")

# Запуск программы
if __name__ == "__main__":
    print("Выберите режим:")
    print("1. Продвинутый светофор с управлением")
    print("2. Простой автоматический светофор")
    print("3. Самый простой светофор")
    
    choice = input("Введите номер (1-3): ").strip()
    
    if choice == "1":
        # Проверяем поддержку select
        try:
            import select
            traffic_light = ConsoleTrafficLight()
            traffic_light.run()
        except ImportError:
            print("На Windows используйте вариант 2 или 3")
            traffic_light = SimpleConsoleTrafficLight()
            traffic_light.run_simple()
            
    elif choice == "2":
        traffic_light = SimpleConsoleTrafficLight()
        traffic_light.run_simple()
        
    elif choice == "3":
        super_simple_traffic_light()
        
    else:
        print("Запускаю простой режим по умолчанию...")
        super_simple_traffic_light()
