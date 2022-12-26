import copy
import os
import time


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Piece():
    def __init__(self, x, y, shape, piece_type):
        self.piece_type = piece_type
        self.shape = shape
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.blocks = self.draw_shape(self.x, self.y)

    def draw_shape(self, x, y):
        return [(x + px, y + py) for px, py in self.shape]

    def move_down(self):
        self.set_pos(self.x, self.y + 1)

    def preview_down(self):
        return self.draw_shape(self.x, self.y + 1)

    def move_left(self):
        self.set_pos(self.x - 1, self.y)

    def preview_left(self):
        return self.draw_shape(self.x - 1, self.y)

    def move_right(self):
        self.set_pos(self.x + 1, self.y)

    def preview_right(self):
        return self.draw_shape(self.x + 1, self.y)


class HorizontalPiece(Piece):
    def __init__(self, x, y):
        self.height_offset = 0
        super().__init__(x, y - self.height_offset,
                         [(0, 0), (1, 0), (2, 0), (3, 0)],
                         HORIZONTAL)


class VerticalPiece(Piece):
    def __init__(self, x, y):
        self.height_offset = 3
        super().__init__(x, y - self.height_offset,
                         [(0, 0), (0, 1), (0, 2), (0, 3)],
                         VERTICAL)


class CrossPiece(Piece):
    def __init__(self, x, y):
        self.height_offset = 2
        super().__init__(x,  y - self.height_offset,
                         [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
                         CROSS)


class AnglePiece(Piece):
    def __init__(self, x, y):
        self.height_offset = 2
        super().__init__(x, y - self.height_offset,
                         [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
                         ANGLE)


class SquarePiece(Piece):
    def __init__(self, x, y):
        self.height_offset = 1
        super().__init__(x, y - self.height_offset,
                         [(0, 0), (0, 1), (1, 0), (1, 1)],
                         SQUARE)


CROSS = 'CROSS'
ANGLE = 'ANGLE'
VERTICAL = 'VERTICAL'
HORIZONTAL = 'HORIZONTAL'
SQUARE = 'SQUARE'

global WIDTH, HEIGHT
WIDTH = 7
HEIGHT = 5000

"""
Notes:
Spawn the piece
preview move, if valid execute, update piece position
continue until piece settled
write checkpoint
spawn new piece

"""


class Canvas():
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.canvas = [['.' for _ in range(width)] for __ in range(height)]
        self.current_piece = None
        self.tallest_point = self.height
        self.spawn_point = (2, self.height - 4)
        # self.checkpoint = None
        # self.add_checkpoint()
        self.piece_count = 0
        self.piece_order = [HORIZONTAL, CROSS, ANGLE, VERTICAL, SQUARE]

    # def add_checkpoint(self):
    #     self.checkpoint = copy.deepcopy(self.canvas)

    def draw_current_piece(self, marker='@'):
        for block_x, block_y in self.current_piece.blocks:
            self.canvas[block_y][block_x] = marker
        # clear()
        # print()
        # for line in self.canvas:
        #     print(''.join(line))
        # print(self.piece_count)
        # time.sleep(0.05)

    def get_piece_type(self):
        return self.piece_order[self.piece_count % len(self.piece_order)]

    def spawn_piece(self, piece_type=None):
        spawn_x, spawn_y = self.spawn_point
        if piece_type == None:
            piece_type = self.get_piece_type()

        if piece_type == CROSS:
            self.current_piece = CrossPiece(spawn_x, spawn_y)
        elif piece_type == ANGLE:
            self.current_piece = AnglePiece(spawn_x, spawn_y)
        elif piece_type == HORIZONTAL:
            self.current_piece = HorizontalPiece(spawn_x, spawn_y)
        elif piece_type == VERTICAL:
            self.current_piece = VerticalPiece(spawn_x, spawn_y)
        elif piece_type == SQUARE:
            self.current_piece = SquarePiece(spawn_x, spawn_y)
        # self.draw_current_piece()
        self.piece_count += 1

    # def wipe_canvas(self):
    #     self.canvas = copy.deepcopy(self.checkpoint)

    def piece_fall(self):
        if self.current_piece is None:
            raise ValueError("No current piece")
        # self.wipe_canvas()
        preview = self.current_piece.preview_down()
        if all(p_y >= 0 and p_y < self.height and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
            self.current_piece.move_down()
            # self.draw_current_piece()
            return True
        else:
            self.draw_current_piece('#')
            # self.add_checkpoint()
            self.tallest_point = min([self.tallest_point] +
                                     [b_y for _, b_y in self.current_piece.blocks])
            self.spawn_point = (2, self.tallest_point - 4)
            self.current_piece = None
            return False

    def piece_push(self, direction):
        if self.current_piece is None:
            raise ValueError("No current piece")
        # self.wipe_canvas()
        if direction == '>':
            preview = self.current_piece.preview_right()
            if all(p_x >= 0 and p_x < self.width and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
                self.current_piece.move_right()
                # self.draw_current_piece()
                return True
            else:
                return False
        elif direction == '<':
            preview = self.current_piece.preview_left()
            if all(p_x >= 0 and p_x < self.width and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
                self.current_piece.move_left()
                # self.draw_current_piece()
                return True
            else:
                return False
        raise ValueError("Unexpected direction", direction)


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return lines[0]


def solve(parsed_lines):
    instructions = list(parsed_lines)
    game_canvas = Canvas()
    game_canvas.spawn_piece()
    while game_canvas.piece_count < 2023:
        print(game_canvas.piece_count)
        can_move = True
        while can_move:
            instruction = instructions.pop(0)
            instructions.append(instruction)
            game_canvas.piece_push(instruction)
            can_move = game_canvas.piece_fall()
        game_canvas.spawn_piece()

    return game_canvas


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    ans = solve(parsed_lines)
    for line in ans.canvas:
        print(''.join(line))
    print(ans.spawn_point)
    print(5000 - ans.spawn_point[1] - 4)
    
