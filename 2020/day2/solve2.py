import re
import attr

# Import lines from file
lines = []
with open('data.txt', 'r') as filehandle:
    for line in filehandle.readlines():
        line = line[:-1]  # remove newline at end of line
        lines.append(line)

# Split the lines into arguments
# Example line: "6-7 w: wwhmzwtwwk"
split_by = "-", " ", ": "
pattern = '|'.join(map(re.escape, split_by))
lines_split = []
for line in lines:
    arguments = re.split(pattern, line)
    lines_split.append(arguments)


# Convert the lines to structured entries
@attr.s
class Entry:
    position1 = attr.ib(converter=int)
    position2 = attr.ib(converter=int)
    letter = attr.ib()
    password = attr.ib()


entries = []
for line_split in lines_split:
    entry = Entry(*line_split)
    entries.append(entry)

# Solve the puzzle with the structured entries
valid_passwords = 0

entry: Entry
for entry in entries:
    position1 = entry.position1 - 1
    position2 = entry.position2 - 1

    position1_has_letter = entry.password[position1] == entry.letter
    position2_has_letter = entry.password[position2] == entry.letter

    is_valid = (position1_has_letter or position2_has_letter) \
        and not (position1_has_letter and position2_has_letter)

    if is_valid:
        print(entry)
        valid_passwords += 1

print("Valid passwords:", valid_passwords)
