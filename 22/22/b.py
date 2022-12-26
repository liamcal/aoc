import re


def read_file(filename='in.txt'):
    with open(filename) as f:
        return [line.strip('\n') for line in f.readlines()]


def parse_map(lines):
    faces = []
    current_face = []
    for line in lines:
        if not line:
            faces.append(current_face)
            current_face = []
        else:
            current_face.append(line)
    faces.append(current_face)
    return faces


def parse_instructions(instruction_line):
    instructions = re.split(r'([RL])', instruction_line[0])
    instructions = list(map(lambda x: x if x == 'L' or x ==
                        'R' else int(x), instructions))
    return instructions


EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

LEFT = -1
RIGHT = +1

moves = [(1, 0),
         (0, 1),
         (-1, 0),
         (0, -1), ]

'''
Heading transition is always opposite destination edge heading

Edge transitions:
East -> West:
    Y1 -> Y2
    XMax1 -> XMin2

East -> East
    Y1 -> -Y2
    XMax1 -> XMax2

East -> South:
    Y1 -> X2
    XMax1 -> YMax2

South -> North: 
    YMax1 -> YMin2
    X1 -> X2

South -> East:
    YMax1 -> XMax2
    X1 -> Y2

West -> East:
    Y1 -> Y2
    XMin1 -> XMax2

West -> West:
    Y1 -> -Y2
    XMin1 -> XMin1

West -> North:
    Y1 -> X2
    XMin1 -> YMin2

North -> South: 
    X1 -> X2
    YMin1 -> YMax2

North -> West:
    YMin1 -> XMin2
    X1 -> Y2
'''

# Real
face_transitions = [
    [(1, WEST), (2, NORTH), (3, WEST), (5, WEST)],
    [(4, EAST), (2, EAST), (0, EAST), (5, SOUTH)],
    [(1, SOUTH), (4, NORTH), (3, NORTH), (0, SOUTH)],
    [(4, WEST), (5, NORTH), (0, WEST), (2, WEST)],
    [(1, EAST), (5, EAST), (3, EAST), (2, SOUTH)],
    [(4, SOUTH), (1, NORTH), (0, NORTH), (3, SOUTH)]]

# # SAMPLE
# face_transitions = [
#     [(5, EAST), (3, NORTH), (2, NORTH), (1, NORTH)],
#     [(2, WEST), (4, SOUTH), (5, SOUTH), (0, NORTH)],
#     [(3, WEST), (4, WEST), (1, EAST), (0, WEST)],
#     [(5, NORTH), (4, NORTH), (2, EAST), (0, SOUTH)],
#     [(5, WEST), (1, SOUTH), (2, SOUTH), (3, SOUTH)],
#     [(0, EAST), (1, WEST), (4, EAST), (3, EAST)]]

# Real
face_offsets = [
    (1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (0, 3)
]

# # Sample
# face_offsets = [
#     (2, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)
# ]


def turn(heading, turn):
    return (heading + turn) % 4


def move(heading, pos):
    step = moves[heading]
    return (pos[0] + step[0], pos[1] + step[1])


def wrap(faces, heading, pos, face):
    width = len(faces[0][0])
    max_x = width - 1
    height = len(faces[0])
    max_y = height - 1
    new_face, new_edge = face_transitions[face][heading]
    # heading opposite from where we just arrived
    new_heading = (new_edge + 2) % 4

    if heading == EAST:
        if new_edge == EAST:
            new_pos = (max_x, max_y - pos[1])
        elif new_edge == SOUTH:
            new_pos = (pos[1], max_y)
        elif new_edge == WEST:
            new_pos = (0, pos[1])
        elif new_edge == NORTH:
            new_pos = (max_x - pos[1], 0)

    elif heading == SOUTH:
        if new_edge == EAST:
            new_pos = (max_x, pos[0])
        elif new_edge == SOUTH:
            new_pos = (max_x - pos[0], max_y)
        elif new_edge == WEST:
            new_pos = (0, max_y - pos[0])
        elif new_edge == NORTH:
            new_pos = (pos[0], 0)

    elif heading == WEST:
        if new_edge == EAST:
            new_pos = (max_x, pos[1])
        elif new_edge == SOUTH:
            new_pos = (max_x - pos[1], max_y)
        elif new_edge == WEST:
            new_pos = (0, max_y - pos[1])
        elif new_edge == NORTH:
            new_pos = (pos[1], 0)

    elif heading == NORTH:
        if new_edge == EAST:
            new_pos = (max_x, max_y - pos[0])
        elif new_edge == SOUTH:
            new_pos = (pos[0], max_y)
        elif new_edge == WEST:
            new_pos = (0, pos[0])
        elif new_edge == NORTH:
            new_pos = (max_x - pos[0], 0)
    try:
        print("Wrapping from", face, pos, heading,
              'to',  new_face, new_pos, new_heading)
        if faces[new_face][new_pos[1]][new_pos[0]] == '.':
            return new_heading, new_pos, new_face
    except IndexError as e:
        print(len(faces))
        print("Failed", height, len(
            faces[new_face]), width, len(faces[new_face[0]]))
        raise e
    return None


def generate_password(heading, pos, face, height, width):
    offset_x, offset_y = face_offsets[face]
    x = pos[0] + offset_x * width + 1
    y = pos[1] + offset_y * height + 1
    return heading + y * 1000 + x * 4


def solve(faces, instructions):
    height = len(faces[0])
    width = len(faces[0][0])

    current_face = 0
    first_row = faces[current_face][0]
    for x, val in enumerate(first_row):
        if val == '.':
            break

    start_pos = (x, 0)
    current_pos = start_pos
    heading = EAST
    history = [(current_face, current_pos, heading)]

    while instructions:
        current_instructions = instructions.pop(0)
        outcome = ''
        # print("Current", current_instructions, "remaining", len(instructions))
        if current_instructions == 'L':
            heading = turn(heading, LEFT)
            outcome = 'Left'
        elif current_instructions == 'R':
            heading = turn(heading, RIGHT)
            outcome = 'Right'
        else:
            distance = current_instructions
            travelled = 0
            while travelled < distance:
                next_pos = move(heading, current_pos)
                if (next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= width or next_pos[1] >= height):
                    wrap_result = wrap(
                        faces, heading, current_pos, current_face)
                    if wrap_result is None:
                        outcome = f'Wall wrap after {travelled}'
                        break

                    new_heading, next_pos, new_face = wrap_result
                    heading = new_heading
                    current_pos = next_pos
                    current_face = new_face

                else:
                    peek_next = faces[current_face][next_pos[1]][next_pos[0]]
                    if peek_next == '.':
                        current_pos = next_pos
                    elif peek_next == '#':
                        outcome = f'Wall after {travelled}'
                        break
                travelled += 1
            if outcome == '':
                outcome = f'Travelled {travelled}'
        history.append((current_face, current_pos, heading,
                       current_instructions, outcome))
    password = generate_password(
        heading, current_pos, current_face, height, width)
    for line in history:
        print(line)
    return password, heading, current_pos, current_face


'''
col 28, 28 * 4 = 112
row 15 + 100 = 115, 115 * 1000 = 115000
'''

if __name__ == '__main__':
    map_contents = read_file('cubeIn.txt')
    instructions_contents = read_file('instructionsIn.txt')
    parsed_lines = parse_map(map_contents)
    parsed_instructions = parse_instructions(instructions_contents)
    print(solve(parsed_lines, parsed_instructions))
