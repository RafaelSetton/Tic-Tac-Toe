from copy import deepcopy


class AI:
    def __init__(self, number):
        self.number = number

    @staticmethod
    def check_win(board):
        conds = (board[0][0] == board[1][1] == board[2][2] != 0,
                 board[2][0] == board[1][1] == board[0][2] != 0)
        if any(conds):
            return board[1][1]
        for x in range(3):
            if board[x][0] == board[x][1] == board[x][2] != 0:
                return board[x][0]
            if board[0][x] == board[1][x] == board[2][x] != 0:
                return board[0][x]
        return 0

    @staticmethod
    def is_full(board):
        return not any([0 in line for line in board])

    def minimax(self, board, depth, maximize: bool):
        score_dict = {self.number: 1, 3-self.number: -1}

        winner = self.check_win(board)
        if winner != 0:
            return score_dict[winner] * (10 - depth)
        elif self.is_full(board):
            return 0
        elif maximize:
            best = -10
            for l in range(3):
                for c in range(3):
                    if board[l][c] == 0:
                        copy = deepcopy(board)
                        copy[l][c] = self.number
                        score = self.minimax(copy, depth + 1, False)
                        best = max(score, best)
            return best
        else:
            best = 10
            for l in range(3):
                for c in range(3):
                    if board[l][c] == 0:
                        copy = deepcopy(board)
                        copy[l][c] = 3 - self.number
                        score = self.minimax(copy, depth + 1, True)
                        best = min(score, best)
            return best

    def best_move(self, board):
        if self.is_full(board) or self.check_win(board) != 0:
            return
        if (board[0] + board[1] + board[2]).count(0) >= 8:
            if board[1][1] == 0:
                board[1][1] = self.number
            else:
                board[0][0] = self.number
                return
        best = -10
        move = tuple()
        for l in range(3):
            for c in range(3):
                if board[l][c] == 0:
                    copy = deepcopy(board)
                    copy[l][c] = self.number
                    score = self.minimax(copy, 0, False)
                    if score > best:
                        best = score
                        move = (l, c)
        board[move[0]][move[1]] = self.number
