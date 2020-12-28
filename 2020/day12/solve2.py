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

    def run(self, ship_x, ship_y, wp_x, wp_y):
        direction = self.direction
        amount = self.amount
        print("Ship", ship_x, ship_y, "Waypoint", wp_x, wp_y, "Command", direction, amount)

        dxs = {'N': 0, 'S': 0, 'E': 1, 'W': -1}
        dys = {'N': 1, 'S': -1, 'E': 0, 'W': 0}

        dx = dxs.get(direction, 0)
        dy = dys.get(direction, 0)

        wp_x += amount * dx
        wp_y += amount * dy

        if direction == 'R':
            times = amount // 90
            for _ in range(times):
                wp_x, wp_y = wp_y, -wp_x

        if direction == 'L':
            times = amount // 90
            for _ in range(times):
                wp_x, wp_y = -wp_y, wp_x

        if direction == 'F':
            ship_x += amount * wp_x
            ship_y += amount * wp_y

        return ship_x, ship_y, wp_x, wp_y

@attr.s(frozen=True)
class Things:
    things = attr.ib()

    @classmethod
    def from_lines(cls, lines):
        things = [Thing.from_string(line) for line in lines]
        return cls(things)

    def run(self):
        ship_x = 0
        ship_y = 0
        wp_x = 10
        wp_y = 1
        for thing in self.things:
            ship_x, ship_y, wp_x, wp_y = thing.run(ship_x, ship_y, wp_x, wp_y)
        return ship_x, ship_y, wp_x, wp_y

lines = open("data.txt").read().split('\n')
things = Things.from_lines(lines)
result = things.run()
print(result, "Anwser2", abs(result[0]) + abs(result[1]))
pass
# 76662 incorrect