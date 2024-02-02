import random
import time

def coloredString(color, string):

    END = "\033[0m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"

    BLACK = "\u001b[40;1m"
    DARK = "\u001b[47;1m"

    if color == 'BLUE':
        return BLUE + string + END
    if color == 'RED':
        return  RED + string + END
    if color == 'GREEN':
        return  GREEN + string + END
    if color == 'YELLOW':
        return YELLOW + string + END
    if color == 'BLACK':
        return BLACK + string + END
    if color == 'DARK':
        return DARK + string + END

class Ship:
    def __init__(self, positions):
        self.positions = positions
        self.hits = []

    def is_sunk(self):
        return len(self.hits) == len(self.positions)

class Board:
    def __init__(self):
        self.board = [['0' for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.hits = set()

    def is_valid_position(self, x, y):
        if not (0 <= x < 6 and 0 <= y < 6):
            return False

        for hit in self.hits:
            if x == hit[0] and y == hit[1]:
                return False

        return True

    def is_hit(self, x, y):
        self.hits.add((x, y))
        for ship in self.ships:
            if (x, y) in ship.positions:
                ship.hits.append((x, y))
                self.board[y][x] = coloredString('RED', '■')
                return True
        self.board[y][x] = coloredString('YELLOW', 'X')
        return False

def get_player_move(board):
    while True:
        try:
            x = int(input("\n" + coloredString("BLUE", "Введите номер столбца (1-6): "))) - 1
            y = int(input(coloredString("BLUE", "Введите номер строки (1-6): "))) - 1
            if (x, y) in board.hits:
                raise ValueError("\n" + coloredString("YELLOW", "Вы уже стреляли в эту клетку!"))
            if not board.is_valid_position(x, y):
                raise ValueError("\n" + coloredString("YELLOW", "Неверный ход!"))
            return x, y
        except ValueError as e:
            print(e)

def get_computer_move(board):
    while True:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        if (x, y) not in board.hits:
            return x, y

def create_random_ships():
    ship_lengths = [3, 2, 2, 1, 1, 1, 1]
    ships = []
    for length in ship_lengths:
        positions = []
        while len(positions) < length:
            valid_positions = []
            for x in range(6):
                for y in range(6):
                    if (x, y) not in positions and Board().is_valid_position(x, y):
                        valid_positions.append((x, y))

            if len(valid_positions) == 0:
                break

            x, y = random.choice(valid_positions)
            positions.append((x, y))
        ships.append(Ship(positions))

    return ships



print(Ship)

def printBoards(player_board, computer_board):
    print("")
    print(coloredString('DARK', "       Доска противника     "), "      ", coloredString('DARK', "         Ваша Доска         "))
    print(coloredString('BLACK', "   | 1 | 2 | 3 | 4 | 5 | 6 |"), "       " + coloredString('BLACK', "   | 1 | 2 | 3 | 4 | 5 | 6 |"))

    for i, row in enumerate(player_board.board):
        computer_row = ["T" if (x, i) in computer_board.hits else "0" if computer_board.board[i][x] == '0' else " " for x in range(6)]
        player_row = [coloredString('GREEN', "■") if (x, i) in [(pos[0], pos[1]) for ship in player_board.ships for pos in ship.positions] else "0" if row[x] == '0' else " " for x in range(6)]

        print(f'{coloredString("BLACK", " " + str(i + 1) + " ")}{"| "}{" | ".join(computer_row)}{" |"}        {coloredString("BLACK", " " + str(i + 1) + " ")}{"| "}{" | ".join(player_row)}{" |"}')

    print("")




def play_game():
    player_board = Board()
    computer_board = Board()

    player_board.ships = create_random_ships()
    computer_board.ships = create_random_ships()

    while True:
        printBoards(player_board, computer_board)

        player_x, player_y = get_player_move(computer_board)

        if computer_board.is_hit(player_x, player_y):
            print("\n", coloredString("GREEN", "Вы попали по кораблю противника!"))
            if all(ship.is_sunk() for ship in computer_board.ships):
                print("\n", coloredString("GREEN", "Вы выиграли!"))
                break
        else:
            print("\n",coloredString("YELLOW", "Вы промахнулись!"))


        computer_x, computer_y = get_computer_move(player_board)

        time.sleep(1)

        if player_board.is_hit(computer_x, computer_y):
            print("\n", coloredString("RED", "Компьютер попал по вашему кораблю!"))
            if all(ship.is_sunk() for ship in player_board.ships):
                print("\n", coloredString("RED", "Компьютер выиграл!"))
                break
        else:
            print("\n", coloredString("GREEN", "Компьютер промахнулся!"))

        time.sleep(2)


play_game()