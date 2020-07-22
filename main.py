from time import sleep
import pygame
pygame.init()


class Game:
    def __init__(self):
        self.SQUARE_SIZE = 200
        self.text_height = 150
        self.tela: pygame.Surface = pygame.display.set_mode((self.SQUARE_SIZE*3, self.SQUARE_SIZE*3 + self.text_height))
        self.board = [[0, 0, 0] for _ in range(3)]
        self.running = True
        self.p1 = {'points': 0, 'figure': self.x, 'num': 1}
        self.p2 = {'points': 0, 'figure': self.o, 'num': 2}
        self.turn = self.p1
        self.font = pygame.font.SysFont('Agency FB', 120, True)

    def x(self, x, y):
        square = self.SQUARE_SIZE
        x *= square
        y *= square
        pygame.draw.line(self.tela, (255, 0, 0), (x + 10, y + 10), (x + square - 10, y + square - 10), 4)
        pygame.draw.line(self.tela, (255, 0, 0), (x + 10, y + square - 10), (x + square - 10, y + 10), 4)

    def o(self, x, y):
        x *= self.SQUARE_SIZE
        y *= self.SQUARE_SIZE
        pos = (int(x + self.SQUARE_SIZE/2), int(y + self.SQUARE_SIZE/2))
        pygame.draw.circle(self.tela, (0, 255, 0), pos, int(self.SQUARE_SIZE/2) - 10, 4)

    def change_turn(self):
        if self.turn == self.p2:
            self.turn = self.p1
        else:
            self.turn = self.p2

    def blit(self):
        # Back Ground
        self.tela.fill((255, 255, 255))
        for i in range(1, 3):
            pygame.draw.line(self.tela, (0, 0, 0), (self.SQUARE_SIZE*i, 0), (self.SQUARE_SIZE*i, 3*self.SQUARE_SIZE), 5)
            pygame.draw.line(self.tela, (0, 0, 0), (0, self.SQUARE_SIZE*i), (3*self.SQUARE_SIZE, self.SQUARE_SIZE*i), 5)

        # Main
        zeros = 0
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 1:
                    self.p1['figure'](x, y)
                elif self.board[x][y] == 2:
                    self.p2['figure'](x, y)
                else:
                    zeros += 1
        if zeros == 0:
            pygame.display.update()
            self.board = [[0, 0, 0] for _ in range(3)]
            sleep(2)

        # Points
        p1 = self.font.render(f"P1: {self.p1['points']}", True, (255, 0, 0))
        p2 = self.font.render(f"P2: {self.p2['points']}", True, (0, 255, 0))
        self.tela.blit(p1, (10, 3 * self.SQUARE_SIZE + 10))
        self.tela.blit(p2, (int(self.tela.get_width() / 2 + 10), 3 * self.SQUARE_SIZE + 10))
        pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                num = 1 if self.turn == self.p1 else 2
                x = event.pos[0]//self.SQUARE_SIZE
                y = event.pos[1]//self.SQUARE_SIZE
                try:
                    if self.board[x][y] == 0:
                        self.board[x][y] = num
                        self.change_turn()
                except IndexError:
                    pass
        if self.check_win() == 0:
            return
        elif self.check_win() == 1:
            self.p1['points'] += 1
        else:
            self.p2['points'] += 1
        self.blit()
        sleep(2)
        self.board = [[0, 0, 0] for _ in range(3)]

    def check_win(self):
        conds = (self.board[0][0] == self.board[1][1] == self.board[2][2] != 0,
                 self.board[2][0] == self.board[1][1] == self.board[0][2] != 0)
        if any(conds):
            return self.board[1][1]
        for x in range(3):
            if self.board[x][0] == self.board[x][1] == self.board[x][2] != 0:
                return self.board[x][0]
            if self.board[0][x] == self.board[1][x] == self.board[2][x] != 0:
                return self.board[0][x]
        return 0

    def loop(self):
        while self.running:
            self.blit()
            self.event_handler()


Game().loop()
