import attr

# Read the data from the file
with open('data.txt') as f:
    lines = f.read().split()


# Split lines into rows and cols and convert to BoardingPass objects
@attr.s
class BoardingPass:
    row_binary = attr.ib()
    col_binary = attr.ib()

    def row_number(self):
        binary = self.row_binary
        binary = binary.replace('F', '0')
        binary = binary.replace('B', '1')
        number = int(binary, 2)
        return number

    def col_number(self):
        binary = self.col_binary
        binary = binary.replace('L', '0')
        binary = binary.replace('R', '1')
        number = int(binary, 2)
        return number

    def seat_id(self):
        return self.row_number() * 8 + self.col_number()


boarding_passes = [BoardingPass(line[0:7], line[7:10]) for line in lines]
# print(*boarding_passes, sep='\n')

# for bp in boarding_passes:
#     print(bp.row_number(), bp.col_number(), bp.seat_id())

seat_ids = [bp.seat_id() for bp in boarding_passes]
seat_ids.sort()
print(seat_ids)

start = seat_ids[0]
end = seat_ids[-1]
missing = sorted(set(range(start, end + 1)).difference(seat_ids))
print(missing)

# 579
