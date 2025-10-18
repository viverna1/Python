import tkinter as tk
from tkinter import ttk


class Application:
    """
    Простое приложение с использованием библиотеки Tkinter.
    """

    def __init__(self):
        """
        Инициализация приложения.
        """
        self.root = tk.Tk()
        self.root.title("Игра")

        self.switch_state = True  # Изначальное состояние переключателя

        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        """
        Создание виджетов приложения.
        """
        # Метка для отображения информации.
        self.label = tk.Label(self.root)
        self.label.grid(row=1, column=0)

        # Кнопка "Показать/Скрыть".
        self.toggle_button = tk.Button(self.root, text="Показать", command=self.toggle_label)
        self.toggle_button.grid(row=0, column=0, padx=40, pady=10)

        # Поле ввода и кнопка "Печатать".
        self.entry = tk.Entry(self.root)
        self.entry.grid(row=1, column=1)
        self.print_button = tk.Button(self.root, text="Печатать", command=self.print_entry)
        self.print_button.grid(row=0, column=1, padx=10, pady=10)

        # Кнопка "Открыть/Закрыть дополнительное окно".
        self.additional_window_button = tk.Button(self.root, text="Открыть дополнительное окно",
                                                  command=self.toggle_additional_window)
        self.additional_window_button.grid(row=0, column=2, padx=10, pady=10)

        # Кнопка "Закрыть программу".
        self.close_button = tk.Button(self.root, text="Закрыть программу", command=self.root.quit)
        self.close_button.grid(row=1, column=2, padx=10, pady=0)

        # Создаем три виджета - два поля, куда можно перетаскивать, и один объект, который будем перетаскивать
        target1 = tk.Label(self.root, text="Цель 1", relief="solid", width=20, height=1)
        target1.grid(row=2, column=0, padx=10, pady=0)

        target2 = tk.Label(self.root, text="Цель 2", relief="solid", width=20, height=1)
        target2.grid(row=2, column=2, padx=10, pady=0)

        drag_drop_widget = DragDropWidget(self.root, text="Перетащи меня!", relief="solid",
                                          target_widgets=[target1, target2])
        drag_drop_widget.grid(row=2, column=1, padx=10, pady=0)

    def toggle_label(self):
        """
        Функция для показа/скрытия метки.
        """
        if self.switch_state:
            self.label.config(text="Кнопка нажата!")
            self.toggle_button.config(text="Скрыть")
        else:
            self.label.config(text="")
            self.toggle_button.config(text="Показать")
        self.switch_state = not self.switch_state

    def print_entry(self):
        """
        Функция для печати содержимого поля ввода.
        """
        entry_text = self.entry.get()
        print(entry_text)

    def toggle_additional_window(self):
        """
        Функция для открытия/закрытия дополнительного окна.
        """
        if not hasattr(self, 'additional_window'):
            self.additional_window_button.config(text="Закрыть дополнительное окно")
            self.additional_window = tk.Toplevel(self.root)
            self.additional_window.title("Дополнительное окно")
            self.additional_window.geometry("200x200")
            self.additional_window.protocol("WM_DELETE_WINDOW", self.close_additional_window)
        else:
            self.additional_window_button.config(text="Открыть дополнительное окно")
            self.additional_window.destroy()
            del self.additional_window

    def close_additional_window(self):
        """
        Функция для закрытия дополнительного окна.
        """
        self.toggle_additional_window()  # Закрываем окно через метод, чтобы удалить его атрибут
        self.additional_window_button.config(text="Открыть дополнительное окно")


class DragDropWidget(ttk.Label):
    def __init__(self, master=None, target_widgets=None, **kwargs):
        super().__init__(master, **kwargs)
        if target_widgets is None:
            target_widgets = []
        self.bind('<ButtonPress-1>', self.on_start_drag)              # Нажатие левой кнопки мыши
        self.bind('<B1-Motion>', self.on_drag)                        # Движение мыши с зажатой левой кнопкой
        self.bind('<ButtonRelease-1>', self.on_drop)                  # Отпускание левой кнопки мыши
        self.bind('<Enter>', lambda event: print("Enter"))            # Наведение указателя мыши на виджет
        self.bind('<Leave>', lambda event: print("Leave"))            # Уход указателя мыши с виджета
        self.bind('<KeyPress>', lambda event: print("KeyPress"))      # Нажатие клавиши
        self.bind('<KeyRelease>', lambda event: print("KeyRelease"))  # Отпускание клавиши
        self.bind('<FocusIn>', lambda event: print("FocusIn"))        # Получение фокуса
        self.bind('<FocusOut>', lambda event: print("FocusOut"))      # Потеря фокуса
        self.bind('<MouseWheel>', lambda event: print("MouseWheel"))  # Прокрутка колеса мыши
        self.bind('<Motion>', lambda event: event)                    # Движение мыши
        self.bind('<Configure>', lambda event: print("Configure"))    # Изменение размеров виджета
        self.bind('<Map>', lambda event: print("Map"))                # Отображение виджета
        self.bind('<Unmap>', lambda event: print("Unmap"))            # Скрытие виджета

        self.target_widgets = target_widgets

    def on_start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        offset_x = event.x - self.start_x
        offset_y = event.y - self.start_y

        x = self.winfo_x() + offset_x
        y = self.winfo_y() + offset_y

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + self.winfo_width() > self.master.winfo_width():
            x = self.master.winfo_width() - self.winfo_width()
        if y + self.winfo_height() > self.master.winfo_height():
            y = self.master.winfo_height() - self.winfo_height()

        self.place(x=x, y=y)

    def on_drop(self, event):
        for target_widget in self.target_widgets:
            if self.is_inside(event, target_widget):
                x = target_widget.winfo_x()
                y = target_widget.winfo_y()
                x_size = target_widget.winfo_width()
                y_size = target_widget.winfo_height()
                x = x + (x_size - self.winfo_width()) / 2
                y = y + (y_size - self.winfo_height()) / 2
                self.place(x=x, y=y)
                break
        else:
            self.place(in_=self.master)

    @staticmethod
    def is_inside(event, widget):
        x, y = event.x_root, event.y_root
        x0, y0, x1, y1 = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(),
                          widget.winfo_rooty() + widget.winfo_height())
        return x0 < x < x1 and y0 < y < y1


# Создание экземпляра класса Application для запуска приложения.
app = Application()
