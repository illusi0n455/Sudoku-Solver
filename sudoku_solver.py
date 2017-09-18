def cross(A, B):
    return [a + b for a in A for b in B]


digits = '123456789'
cols = digits
rows = 'ABCDEFGHI'
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in squares)


def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values


def grid_values(grid):
    chars = [c for c in grid if c in digits + '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values


def display(values):
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join([values[r + c].center(width) + ('|' if c in '36' else '') for c in cols]))
        if r in 'CF':
            print(line)
    print()


def search(values):
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def some(seq):
    for e in seq:
        if e:
            return e
    return False


def solve(grid):
    return search(parse_grid(grid))


# def bulk_solve(filename):
#     """Розвязати судоку взяті в файла"""
#     with open(filename, 'r') as file:
#         sudokus = file.read().split('\n')
#         print("Solving {} sudoku".format(len(sudokus)))
#         results = list(map(solve, sudokus))
#         list(map(display, results))
#         print("Done")
#
#
# bulk_solve('1veryeasy.txt')

# grid1 = '001700509573024106800501002700295018009400305652800007465080071000159004908007053'
# display(solve(grid1))