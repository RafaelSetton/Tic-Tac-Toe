from time import sleep
import pygame
from AI import MiniMaxAI
pygame.init()


class Game:
    def __init__(self):
        self.SQUARE_SIZE = 200
        self.TEXT_HEIGHT = 150
        
        self.tela: pygame.Surface = pygame.display.set_mode((self.SQUARE_SIZE*3, self.SQUARE_SIZE*3 + self.TEXT_HEIGHT))
        self.board = [[0, 0, 0] for _ in range(3)]
        self.running = True
        self.p1 = {'points': 0, 'figure': self.x, 'num': 1}
        self.p2 = {'points': 0, 'figure': self.o, 'num': 2}
        self.turn = self.p1
        self.FONT = pygame.font.SysFont('Agency FB', 120, True)
        self.vsAI = self.choose_mode()
        self.AIPlayer = MiniMaxAI(self.p2['num'])

    def choose_mode(self):
        w = self.tela.get_width()
        h = self.tela.get_height()
        pygame.draw.rect(self.tela, (0, 255, 0), ((0, 100), (w // 2, h - 200)))
        text = self.FONT.render("P v P", True, (255, 255, 255))
        pos = (w//4 - text.get_width()//2, h//2 - text.get_height()//2)
        self.tela.blit(text, pos)

        pygame.draw.rect(self.tela, (255, 0, 0), ((w // 2, 100), (w // 2, h - 200)))
        text = self.FONT.render("P v AI", True, (255, 255, 255))
        pos = (3 * w // 4 - text.get_width() // 2, h // 2 - text.get_height() // 2)
        self.tela.blit(text, pos)

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return event.pos[0] > w//2

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
        if zeros == 0 or self.AIPlayer.check_win(self.board) != 0:
            pygame.display.update()
            sleep(2)

        # Points
        p1 = self.FONT.render(f"P1: {self.p1['points']}", True, (255, 0, 0))
        p2 = self.FONT.render(f"P2: {self.p2['points']}", True, (0, 255, 0))
        self.tela.blit(p1, (10, 3 * self.SQUARE_SIZE + 10))
        self.tela.blit(p2, (int(self.tela.get_width() / 2 + 10), 3 * self.SQUARE_SIZE + 10))
        pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get((pygame.MOUSEBUTTONDOWN, pygame.QUIT)):
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                num = self.turn['num']
                x = event.pos[0]//self.SQUARE_SIZE
                y = event.pos[1]//self.SQUARE_SIZE
                try:
                    if self.board[x][y] == 0:
                        self.board[x][y] = num
                        if self.vsAI:
                            self.blit()
                            sleep(0.5)
                            self.AIPlayer.best_move(self.board)
                            pygame.event.get()
                        else:
                            self.change_turn()
                    self.blit()
                except IndexError:
                    pass
        pygame.event.get()  # Clears Queue
        if self.AIPlayer.check_win(self.board) == 0 and 0 in sum(self.board, []):
            return
        elif self.AIPlayer.check_win(self.board) == 1:
            self.p1['points'] += 1
        elif self.AIPlayer.check_win(self.board) == 2:
            self.p2['points'] += 1
        self.board = [[0, 0, 0] for _ in range(3)]

    def loop(self):
        clock = pygame.time.Clock()
        pygame.event.get()
        while self.running:
            self.blit()
            self.event_handler()
            clock.tick(60)


if __name__ == '__main__':
    Game().loop()
