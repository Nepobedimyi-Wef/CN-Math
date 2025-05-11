import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MathView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("CN-MATH")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.create_main_window()
        self.current_subwindow = None

    def create_main_window(self):
        button = tk.Button(self.root, text="Выключить", height=4, width=20,
                           command=self.root.destroy)
        button.place(x=700, y=700)

        button1 = tk.Button(self.root, text="Построение функции", height=15, width=40,
                            command=self.controller.show_plot_window)
        button1.place(x=100, y=200)

        button2 = tk.Button(self.root, text="Решение уравнения", height=15, width=40,
                            command=self.controller.show_equation_solver)
        button2.place(x=630, y=200)

        button3 = tk.Button(self.root, text="Калькулятор по фотографии", height=15, width=40,
                            command=self.controller.show_image_calculator)
        button3.place(x=1160, y=200)

        button4 = tk.Button(self.root, text="Калькулятор", height=6, width=28,
                            command=self.controller.show_calculator)
        button4.place(x=671, y=550)

    def create_subwindow(self, title, size):
        if self.current_subwindow:
            self.current_subwindow.destroy()

        self.root.withdraw()
        window = tk.Toplevel()
        window.title(title)
        window.geometry(size)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_subwindow(window))
        self.current_subwindow = window
        return window

    def close_subwindow(self, window):
        window.destroy()
        self.current_subwindow = None
        self.root.deiconify()

    def show_plot_window(self, callback):
        window = self.create_subwindow("Построение графика", "600x200")

        tk.Label(window, text="Введите функцию для построения графика (используйте x как переменную):").pack(pady=10)

        entry = tk.Entry(window, width=50)
        entry.pack(pady=5)

        tk.Button(window, text="Построить график",
                  command=lambda: callback(entry.get(), window)).pack(pady=10)

    def show_equation_solver(self, callback):
        window = self.create_subwindow("Решение уравнений", "400x200")

        tk.Label(window, text="Введите уравнение равное 0:").pack()
        equation_entry = tk.Entry(window, width=40)
        equation_entry.pack()

        tk.Label(window, text="Введите переменную:").pack()
        variable_entry = tk.Entry(window, width=10)
        variable_entry.pack()

        tk.Button(window, text="Решить",
                  command=lambda: callback(equation_entry.get(), variable_entry.get(), window)).pack()

    def show_image_calculator(self, callback):
        window = self.create_subwindow("Распознавание математических выражений", "650x450")

        tk.Button(window, text="Выбрать изображение с примером",
                  command=lambda: callback(window)).pack(pady=10)

        self.text_output = tk.Label(window, text="Здесь будет распознанный текст",
                                    wraplength=620, justify='left', anchor='nw')
        self.text_output.pack(expand=True, fill='both', padx=10, pady=10)

        self.result_label = tk.Label(window, text="", font=("Arial", 14), fg='blue')
        self.result_label.pack(pady=10)

    def show_calculator(self, callback):
        window = self.create_subwindow("Калькулятор", "400x200")

        tk.Label(window, text="Введите математический пример:").pack(pady=10)
        self.calc_entry = tk.Entry(window, width=40)
        self.calc_entry.pack(pady=5)

        self.calc_output = tk.Label(window, text="Результат: ")
        self.calc_output.pack(pady=10)

        tk.Button(window, text="Вычислить",
                  command=lambda: callback(self.calc_entry.get(), self.calc_output, window)).pack(pady=10)

    def update_image_calculator(self, text, result):
        self.text_output.config(text=f"Распознанный текст:\n{text}")
        self.result_label.config(text=f"Результат: {result}")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    def ask_open_file(self):
        return filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

    def plot_function(self, x, y, func_str, window):
        plot_window = tk.Toplevel(window)
        plot_window.title("График функции")

        fig = plt.figure(figsize=(10, 5))
        plt.plot(x, y, label=f'y = {func_str}')
        plt.title('График функции')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.grid()
        plt.legend()

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
