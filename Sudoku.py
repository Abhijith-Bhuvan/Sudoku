from random import randint
from time import sleep
from tkinter import *

result = 'Give it a Try!'


def Board_gen(root):
    f = open('Sudoku.txt')
    text = f.read().splitlines()  # Reading the file and splitting into seperate lines.

    # board_num = 'Grid ' + str(randint(1, 50))  # Choosing a random board
    board_num = 'Grid ' + '5'

    for i, line in enumerate(text):
        if board_num == line:
            break

    char_board = [list(line) for line in
                  text[i + 1:i + 10]]  # i+1 to ignore the Grid # line, +1 to the next argument as well.

    for i, line in enumerate(char_board):
        for j, k in enumerate(line):
            if '0' == k:
                char_board[i][j] = '_'  # Converting the blank spaces into _
    f.close()

    # Now we have te board in a 2d character list. We need to put it into a 2d Entry-widget list..

    entry_board = []
    board_values = []

    for i, line in enumerate(char_board):

        temp = []
        val_list = [StringVar() for i in range(9)]
        for j, elm in enumerate(line):
            temp.append(Entry(root, justify=CENTER, textvariable=val_list[j]))

            if '_' == elm:
                if 1 == i and 0 == j:
                    print(' At (' + str(i) + ',' + str(j) + ') spot, the element is = ' + elm)
                temp[j].config(relief=RIDGE, state=NORMAL)

            else:
                temp[j].insert(0, elm)
                temp[j].config(state=DISABLED)

            if 1 == i and 0 == j:
                if '_' == elm:
                    temp[j].config(relief=RIDGE, state=NORMAL)
                else:
                    temp[j].insert(0, elm)
                    temp[j].config(state=DISABLED)

        entry_board.append(temp)
        board_values.append(val_list)

    return board_num, char_board, entry_board, board_values


def Display_board(char_board, root, entry_board):
    line_count = 0
    for line in char_board:
        if 0 == line_count % 3:
            print('~' * 25)
        line_count += 1
        print('| ' + (' ').join(line[:3]) + ' | ' + (' ').join(line[3:6]) + ' | ' + (' ').join(line[6:9]) + ' |')
    print('~' * 25)

    for i in range(9):
        root.grid_rowconfigure(i, weight=1)

        for j in range(9):
            root.grid_columnconfigure(j, weight=1)
            entry_board[i][j].grid(row=i, column=j, sticky=N + S + E + W)


def Check_board(board_values):
    fail = False

    for i in range(9):
        row = []
        for j in range(9):
            val = board_values[i][j].get()
            if '' == val:
                fail = True
                problem = 'Empty cell at (' + str(i + 1) + ',' + str(j + 1) + ')'
                break
            elif not val.isnumeric():
                fail = True
                problem = 'A non-numeric value at (' + str(i + 1) + ',' + str(j + 1) + ') ' + str(val)
                break
            else:
                val = int(val)
            if val <= 0:
                fail = True
                problem = 'A non-positive value at (' + str(i + 1) + ',' + str(j + 1) + ')'
                break
            row.append(val)

        if fail:
            break

        if sorted(row) != list(set(row)):
            fail = True
            problem = 'Repeated numbers in row ' + str(i + 1)
            break

        if 45 != sum(row):
            fail = True
            problem = 'Sum of row ' + str(i + 1) + ' is not equal to 45'
            break

    global result
    if fail:
        result = 'Sorry, that was incorrect.\n\n(Hint: ' + problem + ')'

    else:
        result = 'Congradulations! You won!'


def Solve_board(board_values):  # board_values are a list of pointers to string vars used in entry_board
    # i = row, j = column in board
    i = 0
    while i < 9:
        # try:
        working_row = [int(board_values[i][k].get()) for k in range(9) if board_values[i][k].get() != '']
        unfilled_j = [k for k in range(9) if '' == board_values[i][k].get()]
        # except AttributeError:
        # print('(' + str(i) + ',' + str(k) + ') ' + str(board_values[i][k].get()))

        j = 0
        for j in unfilled_j:
            working_column = [int(board_values[k][j].get()) for k in range(9) if board_values[k][j].get() != '']

            working_num = 1
            while (working_num in working_row) or (working_num in working_column):
                working_num += 1

            board_values[i][j].set(working_num)
            working_row.append(working_num)
        #     # sleep(0.2)
            print('Column = ', working_column)
        print('Row = ', working_row)
        i += 1

    return


def Display(char_board, root, entry_board, board_values):
    global result
    v = StringVar()
    v.set(result)

    Display_board(char_board, root, entry_board)

    check_button = Button(root, text='Check Board', command=lambda: [Check_board(board_values), v.set(result)])
    check_button.grid(row=9, column=0, columnspan=3, sticky=N + S + E + W)

    solve_button = Button(root, text='Auto Solve under work', command=lambda: Solve_board(board_values))
    solve_button.config(state=DISABLED)
    solve_button.grid(row=9, column=5, columnspan=4, sticky=N + S + E + W)

    answer_label = Label(root, textvariable=v, relief=SUNKEN, width=20)
    answer_label.grid(row=10, column=0, padx=5, columnspan=9, sticky=N + S + E + W)


if '__main__' == __name__:
    root = Tk()
    root.title('Sudoku')
    root.geometry('300x300')

    board_num, char_board, entry_board, board_values = Board_gen(root)

    print(board_num)

    Display(char_board, root, entry_board, board_values)

    mainloop()
