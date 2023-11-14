from tkinter import *
import random

# размер сетки 
GRID_SIZE = 9

# для окна GUI
root = Tk()

# сетка 9x9 для судоку
main_sudoku_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Настройка всех ячеек сетки, и создание класса StringVar, позволяющего использовать .set()/.get() для графики
for row in range(GRID_SIZE):
    for column in range(GRID_SIZE):
        main_sudoku_grid[row][column] = StringVar(root)
"""
Основной класс для GUI. 
"""
class MainWindow():
    
    def __init__(self, gui, width, height):

        # Перменные для отображения статуса решения 
        self.SOLVED, self.NOT_SOLVED, self.INCORRECT = "Solved", "Not Solved", "Incorrect!"
        # Определяет правильность разположения решений для выявления результата
        self.solution_status = StringVar(gui)

        self.gui = gui
        gui.title("Sudoku")
        self.width, self.height = width, height
        gui.geometry(f'{width}x{420}')  

        font = ('Arial', 18)
        color = 'white'

        # Настройка кнопок и интерфейса под игровым полем
        Label(root, text = "Generate New Grid",font = ('Helvetica 11 bold')).place( x = 60, y = 290)
        Button(root, text = 'Easy', command  = self.generate_new_grid_easy, bg = 'black', fg = 'white' ).place( x = 20, y = 320)
        Button(root, text = 'Medium', command  = self.generate_new_grid_medium, bg = 'black', fg = 'white').place( x = 103, y = 320)
        Button(root, text = 'Hard', command  = self.generate_new_grid_hard, bg = 'black', fg = 'white').place( x = 210, y = 320)
        Button(root, text = 'Check Solution', command  = self.check_solution, bg = 'black', fg = 'white').place( x = 85, y = 360)
        Label(root, textvariable = self.solution_status, fg='grey',font = ('Helvetica 9 bold')).place( x = self.width/4-5, y = self.height+50)
        # Сетка 9x9, отличается от основной сетки, используется для отображаения в GUI 
        self.gui_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Сетка с правильным решением, для проверки 
        self.correct_solution_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Настройка внешнего вида игрового поля
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):

                if (row < 3 or row > 5) and (column < 3 or column > 5):
                    color = 'gray'
                    dorwd = 0.5
                elif row in [3,4,5] and column in [3,4,5]:
                    color = 'gray'
                    dorwd = 0.5
                else:
                    color = 'white'
                    dorwd = 0
                
                self.gui_grid[row][column] = Entry(gui, width = 2, font = font, bg = color, cursor = 'arrow', borderwidth = 0,
                                                 highlightcolor = 'red', highlightthickness = 1, highlightbackground = 'black',
                                                 textvar = main_sudoku_grid[row][column])
                self.gui_grid[row][column].bind('<Motion>', self.amend_grid)
                self.gui_grid[row][column].bind('<FocusIn>', self.amend_grid)
                self.gui_grid[row][column].bind('<Button-1>', self.amend_grid)
                self.gui_grid[row][column].grid(row=row, column=column)

        # Генерирует новую сетку, легкую по-умолчанию
        self.generate_new_grid_easy()
        
    """
    Исправляет значения в сетке при неверной генерации
    """
    def amend_grid(self, event):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if main_sudoku_grid[row][column].get() == '':
                    continue
                # Проверка корректности чисел (из списка, не двузначные) 
                if len(main_sudoku_grid[row][column].get()) > 1 or main_sudoku_grid[row][column].get() not in ['1','2','3','4','5','6','7','8','9']:
                    main_sudoku_grid[row][column].set('')

    """
    Функция для очистки сетки 
    """
    def clear_grid(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                main_sudoku_grid[row][column].set('')
    """
    Функции генерации новых сеток разной сложности
    """
    def generate_new_grid_easy(self):
        self.clear_grid()
        self.randomize_top_row()
        self.solve_grid()
        self.save_grid()
        self.hide_solution_easy()
        self.solution_status.set(f"Game State: {self.NOT_SOLVED}")

    def generate_new_grid_medium(self):
        self.clear_grid()
        self.randomize_top_row()
        self.solve_grid()
        self.save_grid()
        self.hide_solution_medium()
        self.solution_status.set(f"Game State: {self.NOT_SOLVED}")

    def generate_new_grid_hard(self):
        self.clear_grid()
        self.randomize_top_row()
        self.solve_grid()
        self.save_grid()
        self.hide_solution_hard()
        self.solution_status.set(f"Game State: {self.NOT_SOLVED}")        

    """
    Функция вызова класса StringVar
    """
    def solve_grid(self):
        solution = SolveSudoku()  

    """
    Рандомайзер верной строки, для генерации разных вариантов
    """
    def randomize_top_row(self):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        number_choice = random.sample(number_list, len(number_list))

        for n in range(GRID_SIZE):
            main_sudoku_grid[0][n].set(number_choice[n])

    """
    Функции очищают случайные ячейки от цифр, в зависимости от выбранной сложности 
    """
    def hide_solution_easy(self):
        # Определяет частоту пустых яцеек
        CHANCE_TO_HIDE = 60
        for column in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                # Генератор чисет от 1 до 100
                random_roll = random.randint(0, 100)
                # Если число меньше CHANCE_TO_HIDE
                if random_roll < CHANCE_TO_HIDE:
                    # Очищаем поле(делаем пустым)
                    main_sudoku_grid[row][column].set('')

    def hide_solution_medium(self):
        CHANCE_TO_HIDE = 77
        for column in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                random_roll = random.randint(0, 100)
                if random_roll < CHANCE_TO_HIDE:
                    main_sudoku_grid[row][column].set('')

    def hide_solution_hard(self):
        CHANCE_TO_HIDE = 87
        for column in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                random_roll = random.randint(0, 100)
                if random_roll < CHANCE_TO_HIDE:
                    main_sudoku_grid[row][column].set('')

    """
    # Сохраняет сгенерированную сетку, чтобы check_solution() могла сопоставить правильность ответов
    """
    def save_grid(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                self.correct_solution_grid[row][column] = main_sudoku_grid[row][column].get()

    """
    # Проверяет каждую ячейку на правильность заполнения
    """
    def is_correct_grid(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if main_sudoku_grid[row][column].get() != self.correct_solution_grid[row][column]:
                    return False
        return True

    """
    # Отображает статус правильности решения
    """
    def check_solution(self):
        if self.is_correct_grid():
            self.solution_status.set(f"Game State: {self.SOLVED}")
        else:
            self.solution_status.set(f"Game State: {self.INCORRECT}")
            

    
"""
# Класс с основной логикой игры 
"""
class SolveSudoku():
    
    def __init__(self):
        self.set_all_zero()
        self.sudoku_solve()

    """
    # Задает пустым ячейкам значение '0'
    """
    def set_all_zero(self):
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if main_sudoku_grid[row][column].get() not in ['1','2','3','4','5','6','7','8','9']:
                    main_sudoku_grid[row][column].set(0)

    
    """
    # Алгоритм определения правильности решения
    """
    def sudoku_solve(self, i=0, j=0):
        i,j = self.fill_next_cell(i, j)

        # Если i равен -1, судоку решен
        if i == -1:
            return True
        for e in range(1,10):
            if self.is_valid_cell(i,j,e):
                main_sudoku_grid[i][j].set(e)
                if self.sudoku_solve(i, j):
                    return True
                # Назначет ячейке обратно '0' 
                main_sudoku_grid[i][j].set(0)
        return False

    """
    # Ищет ячейки для заполнения, среди ближайших
    """
    def fill_next_cell(self, i, j):
        for row in range(i, GRID_SIZE):
            for column in range(j, GRID_SIZE):
                if main_sudoku_grid[row][column].get() == '0':
                    return row,column

        for row in range(0, GRID_SIZE):
            for column in range(0, GRID_SIZE):
                if main_sudoku_grid[row][column].get() == '0':
                    return row,column

        return -1,-1

    """
    # Проверяет правильность заполнения main_sudoku_grid[row][column] 
    """
    def is_valid_cell(self, row, column, e):
        # Проверяем строки
        for x in range(GRID_SIZE):
            if main_sudoku_grid[row][x].get() == str(e):
                return False
        # Проверяем столбцы
        for x in range(GRID_SIZE):
            if main_sudoku_grid[x][column].get() == str(e):
                return False

        # Проверяем квадраты 3х3   
        secTopX, secTopY = 3 *int((row/3)), 3 *int((column/3))
        for row in range(secTopX, secTopX+3):
            for column in range(secTopY, secTopY+3):
                if main_sudoku_grid[row][column].get() == str(e):
                    return False
        
        return True



# Запускаем класс основного GUI 
sudoku_application = MainWindow(root, 270, 340)

# Запускаем tkinter mainloop для дисплея непосредственной игры
root.mainloop()
