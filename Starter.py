import pygame
import pygame_menu
from tkinter import *
from random import shuffle
from subprocess import call


pygame.init()
screen = pygame.display.set_mode((540, 540))
pygame.display.set_caption("Boring Games")

def main():
    menu = pygame_menu.Menu('Boring Games', 540, 540,
                        theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('15-puzzle', fifteen_start)
    menu.add.button('Sudoku', sudoku_start)
    menu.add.button('Tic Tac Toe', tictactoe_start)
    menu.add.button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    

def fifteen_start():
    draw_board()
    root.mainloop()

def sudoku_start():
    call(["python", "sudoku.py"])

def tictactoe_start():
    call(["python", "tic_tac_toe.py"])

####################### FIFTEEN-PAZZLE ###############################################################

BOARD_SIZE = 4
SQUARE_SIZE = 80
EMPTY_SQUARE = BOARD_SIZE ** 2

# для окна GUI
root = Tk()
root.title("15-puzzle")

tag_screen = Canvas(root, width=BOARD_SIZE * SQUARE_SIZE,
           height=BOARD_SIZE * SQUARE_SIZE, bg='#727272')
tag_screen.pack()

"""
Считает количество перемещений
"""
def get_inv_count():
    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(EMPTY_SQUARE)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i+1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions

"""
Определяет имеет ли головоломка рещение
"""
def is_solvable():
    num_inversions = get_inv_count()
    if BOARD_SIZE % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = BOARD_SIZE - (board.index(EMPTY_SQUARE) // BOARD_SIZE)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_square(index):
    # Индекс пустой клетки в списке
    empty_index = board.index(EMPTY_SQUARE)
    # Расстояние от пустой клетки до клетки по которой кликнули
    abs_value = abs(empty_index - index)
    # Если пустая клетка над или под клектой на которую кликнули возвращаем индекс пустой клетки
    if abs_value == BOARD_SIZE:
        return empty_index
    # Если пустая клетка слева или справа
    elif abs_value == 1:
        # Проверяем, что блоки в одном ряду
        max_index = max(index, empty_index)
        if max_index % BOARD_SIZE != 0:
            return empty_index
    # Если рядом с клеткой не было пустой
    return index


def draw_board():
    # Удаляет все с освобожденной клетки
    tag_screen.delete('all')
    # Группируем пятнашки из списка в квадрат со сторонами BOARD_SIZE/BOARD_SIZE, (i, j) координаты каждой отдельной пятнашки
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # получаем значение, которое перенесено на клетку
            index = str(board[BOARD_SIZE * i + j])
            # если это не клетка которую мы хотим оставить пустой
            if index != str(EMPTY_SQUARE):
                # рисуем квадрат по заданным координатам
                tag_screen.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE,
                                   j * SQUARE_SIZE + SQUARE_SIZE,
                                   i * SQUARE_SIZE + SQUARE_SIZE,
                                   fill='#363636',
                                   outline='#FFFFFF')
                # пишем число в центре клетки
                tag_screen.create_text(j * SQUARE_SIZE + SQUARE_SIZE / 2,
                              i * SQUARE_SIZE + SQUARE_SIZE / 2,
                              text=index,
                              font="Arial {} italic".format(int(SQUARE_SIZE / 4)),
                              fill='#FFFFFF')


def show_victory_plate():
    # Рисуем серое пле по центру поля
    tag_screen.create_rectangle(SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 - 10 * BOARD_SIZE,
                       BOARD_SIZE * SQUARE_SIZE - SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 + 10 * BOARD_SIZE,
                       fill='#727272',
                       outline='#FFFFFF')
    # Пишем красным WIN на сером поле
    tag_screen.create_text(SQUARE_SIZE * BOARD_SIZE / 2, SQUARE_SIZE * BOARD_SIZE / 1.9,
                  text="WIN!", font="Helvetica {} bold".format(int(10 * BOARD_SIZE)), fill='#DC143C')


def click(event):
    # Получаем координаты клика
    x, y = event.x, event.y
    # Конвертируем координаты из пикселей в клеточки
    x = x // SQUARE_SIZE
    y = y // SQUARE_SIZE
    # Получаем индекс в списке объекта по которому нажали
    board_index = x + (y * BOARD_SIZE)
    # Получаем индекс пустой клетки в списке
    empty_index = get_empty_square(board_index)
    # Меняем местами пустую клетку и клетку, по которой кликнули
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # Перерисовываем игровое поле 
    draw_board()
    # Если текущее состояние доски соответствует правильному - рисуем сообщение о победе
    if board == correct_board:
        # Запускаем фунцию отображения победы
        show_victory_plate()


tag_screen.bind('<Button-1>', click)
tag_screen.pack()


board = list(range(1, EMPTY_SQUARE + 1))
correct_board = board[:]
shuffle(board)

while not is_solvable():
    shuffle(board)

######################## SUDOKU ###################################################



######################## Tic Tac Toe #############################################



###################################################################################

if __name__ == "__main__":
    main()

