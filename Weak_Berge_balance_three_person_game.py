import tkinter as tk
from tkinter import filedialog, simpledialog
import numpy as np
import pygambit as gbt
import json


def load_tensor_from_file(filepath, shape):
    """Загружает тензор из файла .txt."""
    try:
        data = np.loadtxt(filepath, dtype=int)
        if data.size != np.prod(shape):
            raise ValueError(f"Размер данных в файле ({data.size}) не соответствует заданной форме ({shape}).")
        return data.reshape(shape)
    except FileNotFoundError:
        return None
    except ValueError as e:
        print(f"Ошибка при загрузке тензора из файла {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при загрузке тензора из файла {filepath}: {e}")
        return None


def solve_game():
    """Загружает тензоры, решает игру и отображает результат."""
    filepath1 = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    filepath2 = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    filepath3 = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if not all([filepath1, filepath2, filepath3]): #check if all files selected
        result_label.config(text="Ошибка: Выберите все три файла.")
        return

    try:
        shape_str = simpledialog.askstring("Ввод размера", "Введите размер тензора (например, 3,2,4):", initialvalue="3,2,4")
        if shape_str is None: # User canceled input
            return
        shape = tuple(map(int, shape_str.split(',')))
    except ValueError:
        result_label.config(text="Ошибка: Неверный формат размера.  Введите числа, разделенные запятыми (например, 3,2,4).")
        return

    t_1 = load_tensor_from_file(filepath1, shape)
    t_2 = load_tensor_from_file(filepath2, shape)
    t_3 = load_tensor_from_file(filepath3, shape)

    if t_1 is None or t_2 is None or t_3 is None:
        result_label.config(text="Ошибка загрузки тензоров.")
        return

    try:
        A_1 = t_2 + t_3
        B_1 = t_1 + t_3
        C_1 = t_1 + t_2

        g = gbt.Game.from_arrays(A_1, B_1, C_1)
        s = gbt.nash.logit_solve(g)  # or other solver as needed
        equilibria = s.equilibria
        data = json.loads(str(equilibria[0]))
        formatted_rows = []
        for row in data:
            formatted_row = "[" + ", ".join(f"{x:.6f}" for x in row) + "]\n"  # 6 знаков после запятой
            formatted_rows.append(formatted_row)
        formatted_data = "".join(formatted_rows)
        result_label.config(text=f"Равновесия Нэша : \n{formatted_data}")
    except Exception as e:
        result_label.config(text=f"Ошибка при решении игры: {e}")




# Main window setup
root = tk.Tk()
root.title("Решение игры")

load_button = tk.Button(root, text="Загрузить тензоры выигрыша и решить игру", command=solve_game)
load_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

root.mainloop()
