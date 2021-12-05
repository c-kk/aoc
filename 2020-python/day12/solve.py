import attr

@attr.s(frozen=True)
class Thing:
    direction = attr.ib()
    amount = attr.ib(converter=int)

    @classmethod
    def from_string(cls, string):
        direction = string[0]
        amount = string[1:]
        return cls(direction, amount)

    def run(self, x, y, facing):
        direction = self.direction
        amount = self.amount
        # print(x, y, facing, direction, amount)

        if direction == 'R':
            facing += amount

        if direction == 'L':
            facing -= amount

        if direction == 'F':
            divided = facing // 90
            while 3 < divided:
                divided -= 4

            while 0 > divided:
                divided += 4

            direction = {0: 'E', 1: 'S', 2: 'W', 3: 'N'}.get(divided)

        dxs = {'N': 0, 'S': 0, 'E': 1, 'W': -1}
        dys = {'N': 1, 'S': -1, 'E': 0, 'W': 0}

        dx = dxs.get(direction, 0)
        dy = dys.get(direction, 0)

        x += amount * dx
        y += amount * dy

        return x, y, facing

@attr.s(frozen=True)
class Things:
    things = attr.ib()

    @classmethod
    def from_lines(cls, lines):
        things = [Thing.from_string(line) for line in lines]
        return cls(things)

    def run(self):
        x = 0
        y = 0
        facing = 0
        for thing in self.things:
            x, y, facing = thing.run(x, y, facing)
        return x, y, facing


lines = open("2020/day12/data.txt").read().split('\n')
things = Things.from_lines(lines)
result = things.run()
print(result, "Anwser1", abs(result[0]) + abs(result[1]))
pass
