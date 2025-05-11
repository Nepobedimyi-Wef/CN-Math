from model import MathModel
from view import MathView


class MathController:
    def __init__(self):
        self.model = MathModel()
        self.view = MathView(self)

    def show_plot_window(self):
        self.view.show_plot_window(self.handle_plot)

    def show_equation_solver(self):
        self.view.show_equation_solver(self.handle_equation)

    def show_image_calculator(self):
        self.view.show_image_calculator(self.handle_image_calc)

    def show_calculator(self):
        self.view.show_calculator(self.handle_calculation)

    def handle_plot(self, func_str, window):
        try:
            if not func_str:
                self.view.show_error("Ошибка", "Введите функцию для построения")
                return

            x, y = self.model.plot_function(func_str)
            self.view.plot_function(x, y, func_str, window)
        except Exception as e:
            self.view.show_error('Ошибка', f"Ошибка при построении графика: {e}")

    def handle_equation(self, equation_str, variable_str, window):
        try:
            if not equation_str or not variable_str:
                self.view.show_error("Ошибка", "Введите уравнение и переменную")
                return

            solutions = self.model.solve_equation(equation_str, variable_str)
            self.view.show_message("Решение", f"Решения уравнения {equation_str} = 0: {solutions}")
        except Exception as e:
            self.view.show_error("Ошибка", str(e))

    def handle_image_calc(self, window):
        file_path = self.view.ask_open_file()
        if not file_path:
            self.view.show_warning("Предупреждение", "Файл не выбран.")
            return

        try:
            text = self.model.process_image(file_path)
            result = self.model.evaluate_expression(text)
            self.view.update_image_calculator(text, result)
        except Exception as e:
            self.view.show_error("Ошибка", str(e))

    def handle_calculation(self, expression, output_label, window):
        try:
            if not expression:
                self.view.show_error("Ошибка", "Введите выражение для вычисления")
                return

            result = self.model.evaluate_expression(expression)
            output_label.config(text=f"Результат: {result}")
        except Exception as e:
            self.view.show_error("Ошибка", f"Ошибка вычисления: {e}")

    def run(self):
        self.view.run()

if __name__ == "__main__":
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Tesseract OCR не установлен или не добавлен в PATH")
        root.destroy()
        exit()

    app = MathController()
    app.run()
