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

global WIDTH, HEIGHT, MAX_BLOCKS
WIDTH = 7
# This just needs to be big enough for working space, trial and error
HEIGHT = 400
MAX_BLOCKS = 1000000000000


class Canvas():
    def __init__(self, instructions, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.instructions = instructions
        self.instruction_number = 0
        self.canvas = ['.' * width] * height
        self.current_piece = None
        self.tallest_point = self.height
        self.spawn_point = (2, self.height - 4)
        self.piece_count = 0
        self.piece_order = [HORIZONTAL, CROSS, ANGLE, VERTICAL, SQUARE]
        self.y_offset = 0
        self.hashes = {}

    def draw_current_piece(self, marker='@'):
        for block_x, block_y in self.current_piece.blocks:
            current_row = self.canvas[block_y]
            self.canvas[block_y] = current_row[:block_x] + \
                marker + current_row[block_x+1:]

    def get_piece_type(self):
        return self.piece_order[self.piece_count % len(self.piece_order)]

    def spawn_piece(self, piece_type=None):
        spawn_x, spawn_y = self.spawn_point
        if self.spawn_point[1] <= 0:
            raise ValueError(
                "Insufficient working canvas space, tried to spawn a new piece above working area", self.spawn_point)
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
        self.piece_count += 1

    def get_tower_height(self):
        return self.height - self.tallest_point + self.y_offset

    def try_find_cycle(self):
        blocked_cols = set()
        for y in range(2):
            for x in range(self.width):
                if self.canvas[self.tallest_point + y][x] == '#':
                    blocked_cols.add(x)
        if len(blocked_cols) == 7:
            # We found two rows that block the rest of the grid, so we can remove the bottom part,
            # which will allow us to eventually detect a cycle
            truncate_point = self.tallest_point + 2
            truncate_amount = self.height - truncate_point
            self.y_offset += truncate_amount
            self.tallest_point += truncate_amount
            self.canvas = ['.' * self.width] * truncate_amount + \
                self.canvas[:truncate_point]

        flat_canvas = tuple(self.canvas)
        hsh = f'{hash(flat_canvas)}|{self.current_piece.piece_type}|{self.instruction_number % len(self.instructions)}'

        if hsh in self.hashes:
            prev_piece_count, prev_tower_height = self.hashes[hsh]
            cycle_len = self.piece_count - prev_piece_count
            if cycle_len < (MAX_BLOCKS - self.piece_count):
                cycle_height = self.get_tower_height() - prev_tower_height
                cycle_count = (MAX_BLOCKS - self.piece_count) // cycle_len
                # print(
                #     f'Skipping ahead from {self.piece_count}: {cycle_count} cycles of length {cycle_len} with height {cycle_height}')
                self.piece_count += cycle_count * cycle_len
                self.y_offset += cycle_count * cycle_height

        else:
            self.hashes[hsh] = (self.piece_count, self.get_tower_height())

    def piece_fall(self):
        if self.current_piece is None:
            raise ValueError("No current piece")
        preview = self.current_piece.preview_down()
        if all(p_y >= 0 and p_y < self.height and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
            self.current_piece.move_down()
            return True
        else:
            self.draw_current_piece('#')
            self.tallest_point = min([self.tallest_point] +
                                     [b_y for _, b_y in self.current_piece.blocks])
            if self.tallest_point < self.height - 1:
                self.try_find_cycle()  # here's the magic
            self.spawn_point = (2, self.tallest_point - 4)
            self.current_piece = None
            return False

    def consume_instruction(self):
        instruction = self.instructions[self.instruction_number % len(
            self.instructions)]
        self.piece_push(instruction)
        self.instruction_number += 1

    def piece_push(self, direction):
        if self.current_piece is None:
            raise ValueError("No current piece")
        if direction == '>':
            preview = self.current_piece.preview_right()
            if all(p_x >= 0 and p_x < self.width and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
                self.current_piece.move_right()
                return True
            else:
                return False
        elif direction == '<':
            preview = self.current_piece.preview_left()
            if all(p_x >= 0 and p_x < self.width and self.canvas[p_y][p_x] == '.' for p_x, p_y in preview):
                self.current_piece.move_left()
                return True
            else:
                return False
        raise ValueError("Unexpected direction", direction)


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def parse_lines(lines):
    return list(lines[0])


def solve(parsed_lines):
    instructions = parsed_lines
    game_canvas = Canvas(instructions)
    game_canvas.spawn_piece()
    while game_canvas.piece_count <= MAX_BLOCKS:
        can_move = True
        while can_move:
            game_canvas.consume_instruction()
            can_move = game_canvas.piece_fall()
        game_canvas.spawn_piece()

    return game_canvas.get_tower_height()


if __name__ == '__main__':
    lines = read_file()
    parsed_lines = parse_lines(lines)
    print(solve(parsed_lines))
