from random import randint

#manage exeptions
class Exeptions(Exception):
     pass

class OutExeption(Exeptions):
    def __str__(self):
        return "Shot is out of border"

class AlreadyHitExeption(Exeptions):
    def __str__(self):
        return "You've alredy hit this field"

class BoardWrongShipException(Exeptions):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #check if coordinates of two dots are equal
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot:{self.x}, {self.y}'

class Ship:
    #orientation - 0(horizontal), 1(vertical)
    def __init__(self, bow, len, orient):
        self.bow = bow
        self.l = len
        self.o = orient
        self.lifes = len

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            pos_x = self.bow.x
            pos_y = self.bow.y

            #draw ship horizontally
            if self.o == 0:
                pos_x += 1

            # draw ship vertically
            elif self.o == 1:
                pos_y += 1

            ship_dots.append(Dot(pos_x, pos_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    #hid - check if we need to hide the board
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        #how many ships are shot
        self.count = 0

        self.field = [[" "] * size for x in range(size)]

        #busy fields
        self.busy = []
        self.ships = []

    #show the board
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", " ")
        return res

    #check if dot is inside the board (between 0 to size)
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    #verb - put dots on busy spots
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                #check if spot is taken
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        #add contour around ship
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise OutExeption()

        if d in self.busy:
            raise AlreadyHitExeption()

        #add field to busy list
        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    #increase number of killed ships
                    self.count += 1
                    #show contour around dead ship
                    self.contour(ship, verb=True)
                    print("Ship deatroyed!")
                    return False
                else:
                    print("Ship damaged!")
                    #need to repeate turn
                    return True

        self.field[d.x][d.y] = "."
        print("You missed!")
        return False

    #if start new game
    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except Exceptions as e:
                print(e)

class AI(Player):
    def ask(self):
        #generates two random dots
        d = Dot(randint(0,5), randint(0, 5))
        print(f"AI's move: {d.x+1} {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn: ").split()

            if len(cords) != 2:
                print(" Enter 2 coordinates! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Enter numbers! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        #creates two boards
        #player board
        pl = self.random_board()
        #computer board
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    #creates bord with ships
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        #how many times the board was created
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        #start the game
        board.begin()
        return board

    def greet(self):
        print("--------------")
        print("  Game Start  ")
        print("--------------")
        print(" Enter: x y ")
        print(" x - string  ")
        print(" y - column ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Player:")
            print(self.us.board)
            print("-" * 20)
            print("AI:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("It's your turn!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("AI's turn!")
                repeat = self.ai.move()

            #checks if you need to repeat the turn in case the ship was hit
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Player wins!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("AI wins!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()