import attr

@attr.s(frozen=True)
class Point:
    x: int = attr.ib()
    y: int = attr.ib()

    def add(self, point):
        return Point(self.x + point.x, self.y + point.y)

@attr.s(frozen=True)
class Move:
    direction = attr.ib()
    distance = attr.ib(converter=int)

    @classmethod
    def from_string(cls, string):
        direction, distance = string[0], string[1:]
        return cls(direction, distance)

    def apply_move_to_point(self, point: Point):
        new_point = point
        new_points = []
        for d in range(0, self.distance):
            point_to_add = Point(0, 0)
            if self.direction == "R":
                point_to_add = Point(1, 0)
            if self.direction == "L":
                point_to_add = Point(-1, 0)
            if self.direction == "U":
                point_to_add = Point(0, 1)
            if self.direction == "D":
                point_to_add = Point(0, -1)

            new_point = new_point.add(point_to_add)
            new_points.append(new_point)
        return new_points

@attr.s(frozen=True)
class Path:
    points = attr.ib()

    @classmethod
    def from_string(cls, string):
        moves = [Move.from_string(move) for move in string.split(',')]
        points = [Point(0, 0)]
        for move in moves:
            last_point = points[-1]
            new_points = move.apply_move_to_point(last_point)
            points.extend(new_points)
        return cls(points)

    def find_overlapping_points(self, path):
        return list(set(self.points) & set(path.points))

lines = open("data.txt").read().split('\n')
paths = [Path.from_string(line) for line in lines]
path1 = paths[0]
path2 = paths[1]
overlapping_points = path1.find_overlapping_points(path2)
# overlapping_points.remove(Point(0, 0))

combined_steps_per_overlapping_point = []
for overlapping_point in overlapping_points:
    path1_steps = path1.points.index(overlapping_point)
    path2_steps = path2.points.index(overlapping_point)
    combined_steps = path1_steps + path2_steps
    combined_steps_per_overlapping_point.append(combined_steps)

combined_steps_per_overlapping_point.remove(0)
minimum = min(combined_steps_per_overlapping_point)
print(minimum)
pass







# total = 0
# for mass in lines:
#     fuel = int(mass) // 3 - 2  # divide by 3, round down, subtract 2
#     total += fuel
# print(total)