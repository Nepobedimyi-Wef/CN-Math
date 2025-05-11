import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import sympy as sp
import cv2
from PIL import Image
import pytesseract
import re
from tkinter import Tk, Button, Label, Text, filedialog, Scrollbar, END
def evaluate_expression(expression):
    try:
        expression = re.sub(r'[^0-9+\-*/().]', '', expression)
        if not expression:
            return "Нет выражения для вычисления"

        result = eval(expression)
        return result
    except Exception as e:
        return f"Ошибка вычисления: {str(e)}"

def picture():
    def load_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if not file_path:
            messagebox.showwarning("Предупреждение", "Файл не выбран.")
            return

        try:
            pil_image = Image.open(file_path).convert('RGB')
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            thresh_image = cv2.adaptiveThreshold(
                blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )

            inverted_image = cv2.bitwise_not(thresh_image)

            whitelist_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-=()[]{}^*/√,.'

            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=' + whitelist_chars

            text = pytesseract.image_to_string(inverted_image, lang='eng', config=custom_config)

            text_output.config(text=f"Распознанный текст:\n{text.strip()}")

            result = evaluate_expression(text)
            result_label.config(text=f"Результат: {result}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обработать изображение:\n{str(e)}")

    root3 = Tk()
    root3.title("Распознавание математических выражений")
    root3.geometry("650x450")
    root.withdraw()

    def on_closing():
        root.deiconify()
        root3.destroy()

    try:
        pytesseract.get_tesseract_version()
    except:
        messagebox.showerror("Ошибка", "Tesseract OCR не установлен или не добавлен в PATH")
        root3.destroy()
        return

    load_button = Button(root3, text="Выбрать изображение с примером", command=load_image)
    load_button.pack(pady=10)

    text_output = Label(root3, text="Здесь будет распознанный текст", wraplength=620, justify='left', anchor='nw')
    text_output.pack(expand=True, fill='both', padx=10, pady=10)

    result_label = Label(root3, text="", font=("Arial", 14), fg='blue')
    result_label.pack(pady=10)
    root3.protocol("WM_DELETE_WINDOW", on_closing)
    root3.mainloop()


def plot_function(func_str, x_range=(-10, 10), num_points=1000):
    x = np.linspace(x_range[0], x_range[1], num_points)
    try:
        y = eval(func_str)
    except Exception as e:
        messagebox.showinfo('Ошибка',f"Ошибка при вычислении функции: {e}")
        root.deiconify()
        return

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
    root.deiconify()


def on_plot_button_click():
    root.withdraw()
    root4 = tk.Tk()
    root4.title("Построение графика")
    root4.geometry("600x140")

    label = tk.Label(root4, text="Введите функцию для построения графика")
    label.pack(pady=10)

    entry = tk.Entry(root4, width=50)
    entry.pack(pady=10)

    def on_submit():
        func_input = entry.get()
        root4.destroy()
        plot_function(func_input)

    submit_button = tk.Button(root4, text="Построить график", command=on_submit)
    submit_button.pack(pady=10)

    root4.mainloop()
root = tk.Tk()
root.title("CN-MATH")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

def open():
    root.withdraw()
    def solve_equation(equation_str, variable_str):
        variable = sp.symbols(variable_str)

        equation = sp.sympify(equation_str)

        solutions = sp.solve(equation, variable)

        return solutions
    def on_closing():
        root1.destroy()
        root.deiconify()
    def on_solve():
        equation = equation_entry.get()
        variable = variable_entry.get()

        try:
            root1.destroy()
            solutions = solve_equation(equation, variable)
            result = f"Решения уравнения {equation} = 0: {solutions}"
            messagebox.showinfo("Решение", result)
            root.deiconify()
        except Exception as e:
            root1.destroy()
            messagebox.showerror("Ошибка", str(e))
            root.deiconify()

    root1 = tk.Tk()
    root1.title("Решение уравнений")
    equation_label = tk.Label(root1, text="Введите уравнение равное 0:")
    equation_label.pack()
    root1.protocol("WM_DELETE_WINDOW", on_closing)
    equation_entry = tk.Entry(root1, width=40)
    equation_entry.pack()

    variable_label = tk.Label(root1, text="Введите переменную:")
    variable_label.pack()

    variable_entry = tk.Entry(root1, width=10)
    variable_entry.pack()

    solve_button = tk.Button(root1, text="Решить", command=on_solve)
    solve_button.pack()
    root1.mainloop()

def calc():
    root.withdraw()
    def calculate(entry, output_label):
        def on_closing():
            root.deiconify()
            root5.destroy()
        try:
            expression = entry.get()
            result = eval(expression)  # Вычисляем выражение (опасно для произвольного кода!)
            output_label.config(text=f"Результат: {result}")
            root5.protocol("WM_DELETE_WINDOW", on_closing)
        except SyntaxError:
            messagebox.showerror("Ошибка", "Неверный синтаксис выражения!")
            root5.protocol("WM_DELETE_WINDOW", on_closing)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            root5.protocol("WM_DELETE_WINDOW", on_closing)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
            root5.protocol("WM_DELETE_WINDOW", on_closing)

    def create_calculator(window):
        window.title("Калькулятор")
        window.geometry("400x200")

        # Поле ввода
        entry_label = tk.Label(window, text="Введите математический пример:")
        entry_label.pack(pady=10)

        entry = tk.Entry(window, width=40)
        entry.pack(pady=5)

        # Кнопка вычисления
        calculate_button = tk.Button(
            window,
            text="Вычислить",
            command=lambda: calculate(entry, output_label)
        )
        calculate_button.pack(pady=10)

        # Поле вывода результата
        output_label = tk.Label(window, text="Результат: ")
        output_label.pack(pady=10)

    # Пример использования:
    if __name__ == "__main__":
        root5 = tk.Tk()  # Создаём окно
        create_calculator(root5)  # Передаём его в функцию
        root5.mainloop()


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

button3 = tk.Button(root, text="Калькулятор по фотографии", height=15, width=40, fg='#000',
                    bg='#fff', activebackground='#000',
                    activeforeground='#000', cursor='hand2', command=picture)
button3.place(x=1160, y=200)

button4 = tk.Button(root, text="Калькулятор", height=6, width=28, fg='#000',
                    bg='#fff', activebackground='#000',
                    activeforeground='#000', cursor='hand2',command=calc)
button4.place(x=671, y=550)


root.mainloop()
