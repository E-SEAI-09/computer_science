# Set up variables
board = [" "] * 9
current_player = "X"
is_game_running = True

# THe winning combinations
win_combo = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
    (0, 4, 8), (2, 4, 6) # Diagonals
    ]

#Function that prints the board to the terminal
def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")  

# Main game loop
while is_game_running:
    is_valid_move = False

    while not is_valid_move:
        move = input(f"Player {current_player}, Please enter a number from 0-8: ") # "7"

        if move.isdigit():
            move = int(move) # "7" => 7
            if 0 <= move <= 8:
                if board[move] == " ":
                    is_valid_move = True
                else:
                    print("Spot is already taken")
            else:
                print("Number must be between 0 and 8")
        else:
            print("Invalid input! Please enter a number!")

        # Place the symbol
        board[move] = current_player

        # Check for Win
        for pos1, pos2, pos3 in win_combo:
            if board[pos1] == board[pos2] == board[pos3] and board[pos1] != " ":
                
                # Print the board
                print_board(board)

                print(f"Player {current_player} Wins!")
                is_game_running = False
                break

        # Check for a Tie / Draw
        if " " not in board:
            print_board(board)
            print('It\'s a Tie')
            is_game_running = False

        # Print the board
        print_board(board)

        # Switch player
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

    






