import attr

@attr.s
class Block:
    printed_lines = attr.ib(default=0)
