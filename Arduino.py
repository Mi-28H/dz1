import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

class TrafficLightGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 Виртуальный Светофор")
        self.root.geometry("500x700")
        self.root.configure(bg="#2c3e50")
        
        # Настройка иконки (если есть)
        try:
            self.root.iconbitmap('traffic_light.ico')
        except:
            pass
        
        # Тайминги
        self.RED_TIME = 5
        self.YELLOW_TIME = 2
        self.GREEN_TIME = 5
        
        # Текущее состояние
        self.current_state = "RED"
        self.state_start_time = time.time()
        self.auto_mode = True
        self.running = True
        self.blink_mode = False
        self.blink_state = True
        
        # Цвета для светофора
        self.COLORS = {
            "RED_ON": "#ff3333",
            "RED_OFF": "#4a1a1a",
            "YELLOW_ON": "#ffff33",
            "YELLOW_OFF": "#4a4a1a",
            "GREEN_ON": "#33ff33",
            "GREEN_OFF": "#1a4a1a",
            "BG": "#2c3e50",
            "TEXT": "#ecf0f1"
        }
        
        self.setup_ui()
        self.update_display()
        
        # Запуск основного цикла в отдельном потоке
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg=self.COLORS["BG"], padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="🚦 ВИРТУАЛЬНЫЙ СВЕТОФОР",
            font=("Arial", 24, "bold"),
            bg=self.COLORS["BG"],
            fg=self.COLORS["TEXT"]
        )
        title_label.pack(pady=(0, 30))
        
        # Фрейм для светофора
        traffic_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, bd=3)
        traffic_frame.pack(pady=20)
        
        # Корпус светофора
        light_canvas = tk.Canvas(traffic_frame, width=200, height=500, bg="#34495e", highlightthickness=0)
        light_canvas.pack(padx=20, pady=20)
        
        # Рисуем корпус
        light_canvas.create_rectangle(50, 50, 150, 450, fill="#2c3e50", outline="#95a5a6", width=3)
        
        # Создаем лампы
        self.red_light = light_canvas.create_oval(70, 80, 130, 140, fill=self.COLORS["RED_OFF"], outline="")
        self.yellow_light = light_canvas.create_oval(70, 180, 130, 240, fill=self.COLORS["YELLOW_OFF"], outline="")
        self.green_light = light_canvas.create_oval(70, 280, 130, 340, fill=self.COLORS["GREEN_OFF"], outline="")
        
        # Статус светофора
        self.status_label = tk.Label(
            main_frame,
            text="СТОЙ!",
            font=("Arial", 28, "bold"),
            bg=self.COLORS["BG"],
            fg=self.COLORS["TEXT"]
        )
        self.status_label.pack(pady=20)
        
        # Таймер
        self.timer_label = tk.Label(
            main_frame,
            text="До смены: 5.0 сек.",
            font=("Arial", 16),
            bg=self.COLORS["BG"],
            fg=self.COLORS["TEXT"]
        )
        self.timer_label.pack(pady=10)
        
        # Текущее состояние
        self.state_label = tk.Label(
            main_frame,
            text="Состояние: КРАСНЫЙ",
            font=("Arial", 14),
            bg=self.COLORS["BG"],
            fg=self.COLORS["TEXT"]
        )
        self.state_label.pack(pady=10)
        
        # Панель управления
        control_frame = tk.Frame(main_frame, bg=self.COLORS["BG"])
        control_frame.pack(pady=20)
        
        # Кнопки ручного управления
        btn_style = {"font": ("Arial", 12, "bold"), "width": 10, "height": 2}
        
        btn_red = tk.Button(
            control_frame,
            text="🔴 Красный",
            command=lambda: self.set_lights("RED"),
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            **btn_style
        )
        btn_red.grid(row=0, column=0, padx=5, pady=5)
        
        btn_yellow = tk.Button(
            control_frame,
            text="🟡 Желтый",
            command=lambda: self.set_lights("YELLOW"),
            bg="#f39c12",
            fg="white",
            activebackground="#f1c40f",
            **btn_style
        )
        btn_yellow.grid(row=0, column=1, padx=5, pady=5)
        
        btn_green = tk.Button(
            control_frame,
            text="🟢 Зеленый",
            command=lambda: self.set_lights("GREEN"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            **btn_style
        )
        btn_green.grid(row=0, column=2, padx=5, pady=5)
        
        # Кнопки режимов
        mode_frame = tk.Frame(main_frame, bg=self.COLORS["BG"])
        mode_frame.pack(pady=10)
        
        self.auto_btn = tk.Button(
            mode_frame,
            text="🤖 Авторежим",
            command=self.toggle_auto,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            font=("Arial", 12, "bold"),
            width=12,
            height=2
        )
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        self.blink_btn = tk.Button(
            mode_frame,
            text="🚨 Аварийный",
            command=self.toggle_blink,
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            font=("Arial", 12, "bold"),
            width=12,
            height=2
        )
        self.blink_btn.pack(side=tk.LEFT, padx=5)
        
        # Настройки времени
        settings_frame = tk.Frame(main_frame, bg=self.COLORS["BG"])
        settings_frame.pack(pady=20)
        
        tk.Label(
            settings_frame,
            text="Настройка времени (сек):",
            font=("Arial", 12),
            bg=self.COLORS["BG"],
            fg=self.COLORS["TEXT"]
        ).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Красный
        tk.Label(settings_frame, text="Красный:", bg=self.COLORS["BG"], fg=self.COLORS["TEXT"]).grid(row=1, column=0, padx=5)
        self.red_var = tk.IntVar(value=self.RED_TIME)
        red_spin = tk.Spinbox(settings_frame, from_=1, to=30, textvariable=self.red_var, width=5)
        red_spin.grid(row=1, column=1, padx=5)
        
        # Желтый
        tk.Label(settings_frame, text="Желтый:", bg=self.COLORS["BG"], fg=self.COLORS["TEXT"]).grid(row=2, column=0, padx=5)
        self.yellow_var = tk.IntVar(value=self.YELLOW_TIME)
        yellow_spin = tk.Spinbox(settings_frame, from_=1, to=30, textvariable=self.yellow_var, width=5)
        yellow_spin.grid(row=2, column=1, padx=5)
        
        # Зеленый
        tk.Label(settings_frame, text="Зеленый:", bg=self.COLORS["BG"], fg=self.COLORS["TEXT"]).grid(row=3, column=0, padx=5)
        self.green_var = tk.IntVar(value=self.GREEN_TIME)
        green_spin = tk.Spinbox(settings_frame, from_=1, to=30, textvariable=self.green_var, width=5)
        green_spin.grid(row=3, column=1, padx=5)
        
        # Кнопка применения настроек
        apply_btn = tk.Button(
            settings_frame,
            text="Применить",
            command=self.apply_settings,
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad"
        )
        apply_btn.grid(row=1, column=2, rowspan=3, padx=10)
        
        # Информационная панель
        info_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.SUNKEN, bd=2)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.info_label = tk.Label(
            info_frame,
            text="Светофор работает в автоматическом режиме",
            font=("Arial", 10),
            bg="#34495e",
            fg="#ecf0f1",
            pady=5
        )
        self.info_label.pack()
        
        # Кнопка выхода
        exit_btn = tk.Button(
            main_frame,
            text="🚪 Выход",
            command=self.exit_program,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        exit_btn.pack(pady=10)
        
        # Сохраняем ссылки на элементы
        self.canvas = light_canvas
        self.update_buttons()
        
    def update_display(self):
        """Обновление отображения светофора"""
        # Обновляем цвета ламп
        if self.current_state == "RED":
            self.canvas.itemconfig(self.red_light, fill=self.COLORS["RED_ON"])
            self.canvas.itemconfig(self.yellow_light, fill=self.COLORS["YELLOW_OFF"])
            self.canvas.itemconfig(self.green_light, fill=self.COLORS["GREEN_OFF"])
            self.status_label.config(text="СТОЙ!", fg="#e74c3c")
            state_text = "КРАСНЫЙ"
            
        elif self.current_state == "RED_YELLOW":
            self.canvas.itemconfig(self.red_light, fill=self.COLORS["RED_ON"])
            self.canvas.itemconfig(self.yellow_light, fill=self.COLORS["YELLOW_ON"])
            self.canvas.itemconfig(self.green_light, fill=self.COLORS["GREEN_OFF"])
            self.status_label.config(text="ПРИГОТОВЬТЕСЬ!", fg="#f39c12")
            state_text = "КРАСНЫЙ + ЖЕЛТЫЙ"
            
        elif self.current_state == "GREEN":
            self.canvas.itemconfig(self.red_light, fill=self.COLORS["RED_OFF"])
            self.canvas.itemconfig(self.yellow_light, fill=self.COLORS["YELLOW_OFF"])
            self.canvas.itemconfig(self.green_light, fill=self.COLORS["GREEN_ON"])
            self.status_label.config(text="ИДИТЕ!", fg="#2ecc71")
            state_text = "ЗЕЛЕНЫЙ"
            
        elif self.current_state == "YELLOW":
            self.canvas.itemconfig(self.red_light, fill=self.COLORS["RED_OFF"])
            self.canvas.itemconfig(self.yellow_light, fill=self.COLORS["YELLOW_ON"])
            self.canvas.itemconfig(self.green_light, fill=self.COLORS["GREEN_OFF"])
            self.status_label.config(text="ВНИМАНИЕ!", fg="#f1c40f")
            state_text = "ЖЕЛТЫЙ"
            
        elif self.current_state == "OFF":
            # Все лампы выключены (для мигания)
            self.canvas.itemconfig(self.red_light, fill=self.COLORS["RED_OFF"])
            self.canvas.itemconfig(self.yellow_light, fill=self.COLORS["YELLOW_OFF"])
            self.canvas.itemconfig(self.green_light, fill=self.COLORS["GREEN_OFF"])
            self.status_label.config(text="АВАРИЙНЫЙ РЕЖИМ", fg="#f1c40f")
            state_text = "АВАРИЙНЫЙ"
        
        self.state_label.config(text=f"Состояние: {state_text}")
        
        # Обновляем таймер
        elapsed_time = time.time() - self.state_start_time
        
        if self.current_state == "RED":
            time_left = self.RED_TIME - elapsed_time
        elif self.current_state in ["RED_YELLOW", "YELLOW"]:
            time_left = self.YELLOW_TIME - elapsed_time
        elif self.current_state == "GREEN":
            time_left = self.GREEN_TIME - elapsed_time
        else:
            time_left = 0
            
        if time_left > 0:
            self.timer_label.config(text=f"До смены: {time_left:.1f} сек.")
        else:
            self.timer_label.config(text="Смена сейчас!")
        
        # Обновляем информацию о режиме
        if self.blink_mode:
            mode_text = "Аварийный режим (мигающий желтый)"
        elif self.auto_mode:
            mode_text = "Автоматический режим"
        else:
            mode_text = "Ручное управление"
        self.info_label.config(text=mode_text)
        
        self.update_buttons()
        
    def set_lights(self, state):
        """Установка состояния светофора"""
        self.current_state = state
        self.state_start_time = time.time()
        self.auto_mode = False
        self.blink_mode = False
        self.update_display()
        self.show_message(f"Установлен режим: {state}")
        
    def toggle_auto(self):
        """Переключение автоматического режима"""
        self.auto_mode = not self.auto_mode
        self.blink_mode = False
        if self.auto_mode:
            self.show_message("Автоматический режим включен")
        else:
            self.show_message("Ручное управление")
        self.update_buttons()
        
    def toggle_blink(self):
        """Переключение аварийного режима"""
        self.blink_mode = not self.blink_mode
        self.auto_mode = False
        if self.blink_mode:
            self.show_message("Аварийный режим включен")
            self.current_state = "YELLOW"
            self.state_start_time = time.time()
        else:
            self.show_message("Аварийный режим выключен")
            self.current_state = "RED"
            self.state_start_time = time.time()
        self.update_buttons()
        
    def update_buttons(self):
        """Обновление состояния кнопок"""
        if self.auto_mode:
            self.auto_btn.config(bg="#2980b9", relief=tk.SUNKEN)
        else:
            self.auto_btn.config(bg="#3498db", relief=tk.RAISED)
            
        if self.blink_mode:
            self.blink_btn.config(bg="#d35400", relief=tk.SUNKEN)
        else:
            self.blink_btn.config(bg="#e67e22", relief=tk.RAISED)
        
    def switch_state(self):
        """Автоматическое переключение состояния"""
        if self.current_state == "RED":
            self.current_state = "RED_YELLOW"
            self.show_message("Переключаюсь на КРАСНЫЙ+ЖЕЛТЫЙ")
            
        elif self.current_state == "RED_YELLOW":
            self.current_state = "GREEN"
            self.show_message("Переключаюсь на ЗЕЛЕНЫЙ")
            
        elif self.current_state == "GREEN":
            self.current_state = "YELLOW"
            self.show_message("Переключаюсь на ЖЕЛТЫЙ")
            
        elif self.current_state == "YELLOW":
            self.current_state = "RED"
            self.show_message("Переключаюсь на КРАСНЫЙ")
            
        self.state_start_time = time.time()
        self.update_display()
        
    def check_timeout(self):
        """Проверка таймаута для автоматического переключения"""
        if not self.auto_mode:
            return False
            
        current_time = time.time()
        elapsed_time = current_time - self.state_start_time
        
        if self.current_state == "RED" and elapsed_time >= self.RED_TIME:
            return True
        elif self.current_state in ["RED_YELLOW", "YELLOW"] and elapsed_time >= self.YELLOW_TIME:
            return True
        elif self.current_state == "GREEN" and elapsed_time >= self.GREEN_TIME:
            return True
        
        return False
        
    def apply_settings(self):
        """Применение настроек времени"""
        try:
            self.RED_TIME = self.red_var.get()
            self.YELLOW_TIME = self.yellow_var.get()
            self.GREEN_TIME = self.green_var.get()
            self.show_message("Настройки времени применены")
            self.state_start_time = time.time()  # Сбрасываем таймер
        except:
            self.show_message("Ошибка в настройках времени")
        
    def show_message(self, message):
        """Показ информационного сообщения"""
        self.info_label.config(text=message)
        
    def exit_program(self):
        """Выход из программы"""
        self.running = False
        self.root.quit()
        self.root.destroy()
        
    def run_loop(self):
        """Основной цикл программы"""
        while self.running:
            try:
                # Автоматический режим
                if self.auto_mode and self.check_timeout():
                    self.switch_state()
                    
                # Аварийный режим (мигание)
                if self.blink_mode:
                    current_time = time.time()
                    if current_time - self.state_start_time >= 0.5:
                        self.blink_state = not self.blink_state
                        self.state_start_time = current_time
                        if self.blink_state:
                            self.current_state = "YELLOW"
                        else:
                            self.current_state = "OFF"
                        
                        # Обновляем GUI из главного потока
                        self.root.after(0, self.update_display)
                
                # Обновляем таймер каждые 100 мс
                self.root.after(100, self.update_display)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Ошибка в цикле: {e}")
                break

def main():
    """Запуск программы"""
    root = tk.Tk()
    app = TrafficLightGUI(root)
    
    # Обработка закрытия окна
    def on_closing():
        app.running = False
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
