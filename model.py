import numpy as np
import sympy as sp
import cv2
import re
from PIL import Image
import pytesseract

class MathModel:
    @staticmethod
    def evaluate_expression(expression):
        try:
            expression = re.sub(r'[^0-9+\-*/().]', '', expression)
            if not expression:
                return "Нет выражения для вычисления"
            result = eval(expression)
            return result
        except Exception as e:
            return f"Ошибка вычисления: {str(e)}"

    @staticmethod
    def solve_equation(equation_str, variable_str):
        variable = sp.symbols(variable_str)
        equation = sp.sympify(equation_str)
        solutions = sp.solve(equation, variable)
        return solutions

    @staticmethod
    def process_image(file_path):
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
            return text.strip()
        except Exception as e:
            raise Exception(f"Не удалось обработать изображение: {str(e)}")

    @staticmethod
    def plot_function(func_str, x_range=(-10, 10), num_points=1000):
        x = np.linspace(x_range[0], x_range[1], num_points)
        y = eval(func_str)
        return x, y
