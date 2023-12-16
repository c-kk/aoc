import re
import sys

DAY = 22

TEST = sys.argv[1] == "test" if len(sys.argv) > 1 else False

TEST_DATA = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

if TEST:
    def get_daily_input(_):
        for line in TEST_DATA.strip("\n").split("\n"):
            yield line.strip("\n")


def load_data() -> tuple[list[str], list[str]]:
    data_stream = open('data2.txt').read().split('\n')
    map_data: list[str] = []
    path_data: list[str] = []
    for d in data_stream[0:-2]:
        map_data.append(d)
    path_data = re.findall(r"\d+|[LR]", data_stream[-1])
    width = max(len(m) for m in map_data)
    return list([m.ljust(width) for m in map_data]), path_data


class MonkeyMap:
    adjacent = {
        "u": "rflb", "d": "rblf",
        "f": "rdlu", "b": "ldru",
        "l": "fdbu", "r": "bdfu"
    }

    facings = ">v<^"

    def __init__(self, mm):
        self.map = mm
        self.height = len(mm)
        self.width = len(mm[0])
        self.face_size = self.find_face_size(self.height, self.width)
        self.face_map = self.build_face_map()

    def build_face_map(self):
        def _add_sides(r_in: int, c_in: int) -> None:
            cf, ce = face_map[r_in][c_in]

            for r, c, d, e in [(r_in - 1, c_in, 3, 1), (r_in + 1, c_in, 1, 3),
                               (r_in, c_in - 1, 2, 0), (r_in, c_in + 1, 0, 2)]:
                if 0 <= r < len(face_map) \
                        and 0 <= c < len(face_map[0]) \
                        and not face_map[r][c] \
                        and self.map[r * self.face_size][c * self.face_size] != " ":
                    nf = ce[d]
                    ne = self.adjacent[nf]
                    while ne[e] != cf:
                        ne = ne[1:] + ne[0]
                    face_map[r][c] = (nf, ne)
                    _add_sides(r, c)

        face_map: list[list[tuple[str, str] | None]] = [
            [None for _ in range(self.width // self.face_size)]
            for _ in range(self.height // self.face_size)
        ]

        first_face = (0, re.search(r"[.#]", self.map[0]).start() // self.face_size)
        face_map[0][first_face[1]] = ("u", "rflb")
        _add_sides(*first_face)

        return face_map

    def next_position_2d(self, r: int, c: int, f: str) -> tuple[int, int]:
        if f == ">":
            if c + 1 < self.width and self.map[r][c + 1] == ".":
                c += 1
            elif c + 1 >= self.width or self.map[r][c + 1] == " ":
                nc = c
                while nc - 1 >= 0 and self.map[r][nc - 1] != " ":
                    nc -= 1
                if self.map[r][nc] == ".":
                    c = nc
        elif f == "<":
            if c > 0 and self.map[r][c - 1] == ".":
                c -= 1
            elif c - 1 < 0 or self.map[r][c - 1] == " ":
                nc = c
                while nc + 1 < self.width and self.map[r][nc + 1] != " ":
                    nc += 1
                if self.map[r][nc] == ".":
                    c = nc
        elif f == "v":
            if r + 1 < self.height and self.map[r + 1][c] == ".":
                r += 1
            elif r + 1 >= self.height or self.map[r + 1][c] == " ":
                nr = r
                while nr - 1 >= 0 and self.map[nr - 1][c] != " ":
                    nr -= 1
                if self.map[nr][c] == ".":
                    r = nr
        elif f == "^":
            if r > 0 and self.map[r - 1][c] == ".":
                r -= 1
            elif r - 1 < 0 or self.map[r - 1][c] == " ":
                nr = r
                while nr + 1 < self.height and self.map[nr + 1][c] != " ":
                    nr += 1
                if self.map[nr][c] == ".":
                    r = nr

        return r, c

    def next_position_3d(self, r: int, c: int, f: str) -> tuple[int, int, str]:
        def _find_face(target_face: str) -> tuple[int, int]:
            for i in range(len(self.face_map)):
                for j in range(len(self.face_map[i])):
                    if self.face_map[i][j] and self.face_map[i][j][0] == target_face:
                        return i, j

        nr, nc, nf = r, c, f
        if f == ">" and c + 1 < self.width and self.map[r][c + 1] != " ":
            nc += 1
        elif f == "<" and c > 0 and self.map[r][c - 1] != " ":
            nc -= 1
        elif f == "^" and r > 0 and self.map[r - 1][c] != " ":
            nr -= 1
        elif f == "v" and r + 1 < self.height and self.map[r + 1][c] != " ":
            nr += 1
        else:
            cf_name, cf_edges = self.face_map[r // self.face_size][c // self.face_size]
            nf_name = cf_edges[self.facings.find(f)]
            nf_map_row, nf_map_col = _find_face(nf_name)
            nf_edges = self.face_map[nf_map_row][nf_map_col][1]

            nf = self.facings[nf_edges.find(cf_name) - 2]
            nr = nf_map_row * self.face_size + (
                (self.face_size - 1) if nf == "^" else 0
            )
            nc = nf_map_col * self.face_size + (
                (self.face_size - 1) if nf == "<" else 0
            )

            if (f == ">" and nf == "v") or (f == "<" and nf == "^"):   # 90 cw h to v
                nc += self.face_size - 1 - r % self.face_size
            elif (f == "^" and nf == ">") or (f == "v" and nf == "<"):  # 90 cw v to h
                nr += c % self.face_size
            elif (f == ">" and nf == "^") or (f == "<" and nf == "v"):  # 90 ccw h to v
                nc += r % self.face_size
            elif (f == "v" and nf == ">") or (f == "^" and nf == "<"):  # 90 ccw v to h
                nr += self.face_size - 1 - c % self.face_size
            elif (f == ">" and nf == "<") or (f == "<" and nf == ">"):  # 180 horiz
                nr += self.face_size - 1 - r % self.face_size
            elif (f == "^" and nf == "v") or (f == "v" and nf == "^"):  # 180 vert
                nc += self.face_size - 1 - c % self.face_size
            elif (f == "<" and nf == "<") or (f == ">" and nf == ">"):  # 0 horiz
                nr += r % self.face_size
            elif (f == "^" and nf == "^") or (f == "v" and nf == "v"):  # 0 vert
                nc += c % self.face_size

        if self.map[nr][nc] == ".":
            r, c, f = nr, nc, nf

        return r, c, f

    def walk_map(self, path: list[str], cube: bool = False) -> int:
        row, column = 0, self.map[0].find(".")
        facing = ">"

        for p in path:
            if p.isnumeric():
                for _ in range(int(p)):
                    if cube:
                        row, column, facing = self.next_position_3d(row, column, facing)
                    else:
                        row, column = self.next_position_2d(row, column, facing)
            elif p == "L":
                facing = self.facings[self.facings.find(facing) - 1]
            else:
                facing = self.facings[(self.facings.find(facing) + 1) % 4]

        return 1000 * (row + 1) + 4 * (column + 1) + self.facings.find(facing)

    @classmethod
    def find_face_size(cls, h, w) -> int:
        for x, y in [(2, 5), (3, 4), (4, 3), (5, 2)]:
            if h // x == w // y:
                return h // x


def main():
    monkey_map_data, path_data = load_data()
    monkey_map = MonkeyMap(monkey_map_data)
    print(f"Part 1: {monkey_map.walk_map(path_data)}")
    print(f"Part 2: {monkey_map.walk_map(path_data, cube=True)}")


if __name__ == "__main__":
    main()

"""
Part 1: 75254
Part 2: 108311
"""