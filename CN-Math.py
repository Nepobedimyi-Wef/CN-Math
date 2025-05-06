import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import sympy as sp
import cv2
import pytesseract
from tkinter import Tk, Button, Label, Text, filedialog, Scrollbar, END
def picture():
    def load_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not file_path:
            print("Файл не выбран.")  # Отладочное сообщение
            return

        print(f"Выбранный файл: {file_path}")  # Отладочное сообщение

        # Загрузка изображения
        image = cv2.imread(file_path)
        if image is None:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            print("Ошибка: изображение не загружено.")  # Отладочное сообщение
            return root3.destroy()

        print("Изображение успешно загружено.")  # Отладочное сообщение

        # Преобразование в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Применение размытия для уменьшения шума
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        # Использование адаптивного порогового преобразования для лучшего контраста математических символов
        thresh_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 11, 2)

        # Инвертирование изображения (Tesseract читает черный текст на белом фоне)
        inverted_image = cv2.bitwise_not(thresh_image)

        # Разрешенные символы: цифры, буквы и общие математические символы
        whitelist_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-=()[]{}^*/√,.'

        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=' + whitelist_chars

        # Распознавание текста
        text = pytesseract.image_to_string(inverted_image, lang='eng', config=custom_config)

        # Очистка и вставка распознанного текста в текстовое поле
        text_output.delete(1.0, END)
        text_output.insert(END, text)


    # Настройка Tkinter
    root3 = Tk()
    root3.title("OCR для математических выражений")
    root3.geometry("650x450")

    load_button = Button(root3, text="Выбрать изображение с примером", command=load_image)
    load_button.pack(pady=10)

    text_output = Text(root3, wrap='word', height=20)
    text_output.pack(expand=True, fill='both', padx=10, pady=10)

    scrollbar = Scrollbar(text_output)
    scrollbar.pack(side='right', fill='y')
    text_output.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_output.yview)

    root3.mainloop()


def plot_function(func_str, x_range=(-10, 10), num_points=1000):
    # Создаем массив значений x
    x = np.linspace(x_range[0], x_range[1], num_points)

    # Используем eval для вычисления значений функции
    try:
        y = eval(func_str)
    except Exception as e:
        print(f"Ошибка при вычислении функции: {e}")
        return

    # Строим график
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label=f'y = {func_str}')
    plt.title('График функции')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.show()

def on_plot_button_click():
    func_input = entry.get()  # Получаем текст из текстового поля
    plot_function(func_input)

root = tk.Tk()
root.title("World of Math")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

def open():

    def solve_equation(equation_str, variable_str):
        # Определяем переменную
        variable = sp.symbols(variable_str)

        # Преобразуем строку уравнения в символьное выражение
        equation = sp.sympify(equation_str)

        # Решаем уравнение
        solutions = sp.solve(equation, variable)

        return solutions

    def on_solve():
        equation = equation_entry.get()
        variable = variable_entry.get()

        try:
            solutions = solve_equation(equation, variable)
            result = f"Решения уравнения {equation} = 0: {solutions}"
            messagebox.showinfo("Решение", result)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # Создаем окно
    root1 = tk.Tk()
    root1.title("Решение уравнений")

    # Создаем виджеты
    equation_label = tk.Label(root1, text="Введите уравнение равное 0:")
    equation_label.pack()

    equation_entry = tk.Entry(root1, width=40)
    equation_entry.pack()

    variable_label = tk.Label(root1, text="Введите переменную:")
    variable_label.pack()

    variable_entry = tk.Entry(root1, width=10)
    variable_entry.pack()

    solve_button = tk.Button(root1, text="Решить", command=on_solve)
    solve_button.pack()
    root1.mainloop()

label = tk.Label(root, text="Введите функцию для построения графика")
label.place(x=100, y=130)

# Текстовое поле для ввода функции
entry = tk.Entry(root, width=50)
entry.place(x=100, y=160)


button = tk.Button(root, text="Выключить", height=4, width=20, fg='#000',
                   bg='#fff', activebackground='#000',
                   activeforeground='#000', cursor='hand2', command=root.destroy)
button.place(x=700, y=700)

button1 = tk.Button(root, text="Построение функции", height=15, width=40, fg='#000',
                    bg='#fff', activebackground='#000',
                    activeforeground='#000', cursor='hand2', command=on_plot_button_click)
button1.place(x=100, y=200)

button2 = tk.Button(root, text="Решение уравнения", height=15, width=40, fg='#000',
                    bg='#fff', activebackground='#000',
                    activeforeground='#000', cursor='hand2', command=open)
button2.place(x=630, y=200)

button3 = tk.Button(root, text="Калькулятор", height=15, width=40, fg='#000',
                    bg='#fff', activebackground='#000',
                    activeforeground='#000', cursor='hand2', command=picture)
button3.place(x=1160, y=200)

root.mainloop()
