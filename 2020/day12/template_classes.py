import attr

@attr.s(frozen=True)
class Thing:
    var = attr.ib()

    @classmethod
    def from_string(cls, string):
        var = string
        return cls(var)

    def run(self):
        return None

@attr.s(frozen=True)
class Things:
    things = attr.ib()

    @classmethod
    def from_lines(cls, lines):
        things = [Thing.from_string(line) for line in lines]
        return cls(things)

    def run(self):
        return None


lines = open("2020/day9/data.txt").read().split('\n')
things = Things.from_lines(lines)
result = things.run()
print(result)
pass
