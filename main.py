import tkinter as tk
from tkinter import ttk
import math
import re

class Calculator:
    def __init__(self, entry):
        self.entry = entry
        self.entry_font_size = 24
        self.button_font_size = 14

    def set_entry_style(self):
        style = ttk.Style()
        style.configure("TEntry", padding=(5, 5))
        self.entry.config(style="TEntry")
        self.entry.bind("<Configure>", lambda event: self.adjust_font_size(event, self.entry))
        self.entry['validatecommand'] = (self.entry.register(self.validate), '%P')
        self.entry['validate'] = 'key'

    def validate(self, new_text):
        allowed_chars = set('0123456789+-*/.()%=')
        if new_text == '' or new_text == '-' or new_text[0] == '.':
            return True
        return all(char in allowed_chars for char in new_text)

    def set_button_style(self, button):
        style = ttk.Style()
        style.configure("TButton", padding=(2, 2), relief="raised", borderwidth=2, font=('Arial', self.button_font_size))
        button.config(style="TButton")

    def create_button(self, parent, text, command=None, width=5):
        button = ttk.Button(parent, text=text, command=command, width=width)
        self.set_button_style(button)
        button.bind("<Configure>", lambda event: self.adjust_font_size(event, button))
        return button

    def button_click(self, number):
        current = self.entry.get()
        if current == "0" and str(number).isdigit() and len(current) == 1:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(number))
        elif len(current) > 2 and current[-2] in ['+', '*', '/', '-'] and current[-1] == "0":
            self.entry.delete(len(current) - 1, tk.END)
            self.entry.insert(tk.END, str(number))
        else:
            self.entry.insert(tk.END, str(number))
        self.entry.focus_set()

    def button_equal(self):
        current = self.entry.get()
        if current and current[-1] in ['+', '-', '*', '/']:
            current = current[:-1]

        try:
            result = eval(current)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка")
        self.entry.focus_set()

    def button_clear(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, "0")

    def button_percent(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            if len(parts) == 1:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "0")
            elif len(parts) == 3:
                first_number, operator, second_number = map(float, parts)
                if operator in {'+', '-'}:
                    result = first_number + (first_number * (second_number / 100))
                elif operator in {'*', '/'}:
                    result = first_number * (second_number * 0.01)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_clean_entry(self):
        current = self.entry.get()
        if current:
            last_operator_index = max(current.rfind('+'), current.rfind('-'), current.rfind('*'), current.rfind('%'))
            if last_operator_index != -1:
                self.entry.delete(last_operator_index + 1, tk.END)
            else:
                self.entry.delete(0, tk.END)

    def button_backspace_action(self):
        current = self.entry.get()
        if current:
            current = current[:-1]
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current)

    def button_change_sign(self):
        current = self.entry.get()
        if current:
            parts = re.split(r'([-+*/])', current)

            last_number = next((part for part in reversed(parts) if part and part[0].isdigit()), None)

            if last_number:
                updated_number = str(-float(last_number)) if last_number[0] != '-' else last_number[1:]
                updated_input = current.rsplit(last_number, 1)[0] + updated_number
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)

    def button_decimal(self):
        current = self.entry.get()
        if '.' not in current:
            if current and (current[-1].isdigit() or current[-1] == ')'):
                self.entry.insert(tk.END, '.')
            elif len(current) == 1 and current[-1] in ['+', '-', '*', '/']:
                self.entry.insert(tk.END, '0.')
            elif len(current) == 1 and current[-1] == '-':
                self.entry.insert(tk.END, '0.')
            elif not current:
                self.entry.insert(tk.END, '0.')

    def button_inverse(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            last_number = next((part for part in reversed(parts) if part and part[0].isdigit()), None)

            if last_number and float(last_number) != 0:
                result = 1 / float(last_number)
                updated_input = current.rsplit(last_number, 1)[0] + str(result)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Ошибка: Деление на ноль")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_square(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            last_number = next((part for part in reversed(parts) if part and part[0].isdigit()), None)

            if last_number:
                squared_number = str(float(last_number) ** 2)
                updated_input = current.rsplit(last_number, 1)[0] + squared_number
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_square_root_2(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)
            last_number = next((part for part in reversed(parts) if part and part[0].isdigit()), None)

            if last_number:
                result = math.sqrt(float(last_number))
                updated_input = current.rsplit(last_number, 1)[0] + str(result)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Ошибка: Нет числа для извлечения корня")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def adjust_font_size(self, event, widget):
        new_width, new_height = event.width, event.height
        new_font_size = max(10, int(min(new_width / 15, new_height / 2)))
        if new_font_size > 46:
            new_font_size = 46
        if new_font_size != self.entry_font_size:
            self.entry_font_size = new_font_size
            new_font = ('Arial', self.entry_font_size)

            style = ttk.Style()
            style.configure("TEntry", font=new_font)

            widget.config(style="TEntry")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Калькулятор")

    entry_font = ('Arial', 24)
    button_font = ('Arial', 14)

    entry = ttk.Entry(window, width=20, font=entry_font, justify="right")
    entry.bind('<Key>', lambda event: buttons_logic.button_click(event.char))
    entry.bind('<Return>', lambda event: buttons_logic.button_equal())
    buttons_logic = Calculator(entry)
    buttons_logic.set_entry_style()
    entry.grid(row=0, column=0, columnspan=4, sticky="nsew")
    entry.insert(tk.END, "0")

    entry.focus_set()

    buttons = []
    button_labels = [7, 8, 9, 4, 5, 6, 1, 2, 3]

    button_grid_info = [(str(number), lambda number=number: buttons_logic.button_click(number), i // 3 + 3, i % 3) for i, number in enumerate(button_labels)]

    button_data = [
        ("0", lambda: buttons_logic.button_click(0), 6, 1),
        ("+", lambda: buttons_logic.button_click("+"), 5, 3),
        ("-", lambda: buttons_logic.button_click("-"), 4, 3),
        ("\u00D7", lambda: buttons_logic.button_click("*"), 3, 3),
        ("=", buttons_logic.button_equal, 6, 3),
        ("С", buttons_logic.button_clear, 1, 2),
        ("%", buttons_logic.button_percent, 1, 0),
        ("CE", buttons_logic.button_clean_entry, 1, 1),
        ("\u2190", buttons_logic.button_backspace_action, 1, 3),
        ("+/-", buttons_logic.button_change_sign, 6, 0),
        (".", buttons_logic.button_decimal, 6, 2),
        ("1/x", buttons_logic.button_inverse, 2, 0),
        ("x^2", buttons_logic.button_square, 2, 1),
        ("√x", buttons_logic.button_square_root_2, 2, 2),
        ("/", lambda: buttons_logic.button_click("/"), 2, 3),
    ]


    for label, command, row, column in button_grid_info + button_data:
        button = buttons_logic.create_button(window, label, command)
        button.grid(row=row, column=column, sticky="nsew")
        buttons.append(button)

    for i in range(7):
        window.grid_rowconfigure(i, weight=1)

    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    window.minsize(width=300, height=300)
    window.mainloop()
