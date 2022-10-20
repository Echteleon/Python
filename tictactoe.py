the_board = {'7':' ', '8': ' ', '9': ' ',
         '4': ' ', '5': ' ', '6': ' ',
         '1': ' ', '2': ' ', '3': ' '
         }


def print_board(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['1'] + '|' + board['2'] + '|' + board['3'])


def game():
    turn = 'X'
    count = 0

    for i in range(10):
        print_board(the_board)
        print(f"It's your turn({turn}). Where put {turn}?")

        move = input("Enter cell number:")

        if the_board[move] == ' ':
            the_board[move] = turn
            count += 1
        else:
            print('This field is already taken. Choose another field.')
            continue

        if count>=5:
            #top line
            if the_board['7'] == the_board['8'] == the_board['9'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #middle line
            elif the_board['4'] == the_board['4'] == the_board['6'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #bottom line
            elif the_board['1'] == the_board['2'] == the_board['3'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #vertical left
            elif the_board['7'] == the_board['4'] == the_board['1'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #vertical middle
            elif the_board['8'] == the_board['5'] == the_board['2'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #vertical right
            elif the_board['9'] == the_board['6'] == the_board['3'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #diagonal
            elif the_board['9'] == the_board['5'] == the_board['1'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break
            #diagonal 2
            elif the_board['7'] == the_board['5'] == the_board['3'] != ' ':
                print(print_board(the_board))
                print(f"{turn} player won")
                print("Game over")
                break

        #if no one wins
        if count == 9:
            print("It's a tie")
            print("Game over")

        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'

    board_keys = []
    for key in the_board:
        board_keys.append(key)

    restart = input("Do you want to play again? Yes/No")
    if restart == 'yes' or restart == 'Yes':
        for key in board_keys:
            the_board[key] = " "

        game()

print(game())