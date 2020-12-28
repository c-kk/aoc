import re
import attr


# example: "6-7 w: wwhmzwtwwk"
@attr.s(frozen=True)
class Entry(object):
    minimum = attr.ib()
    maximum = attr.ib()
    letter = attr.ib()
    password = attr.ib()


delimiters = "-", " ", ": "
regexPattern = '|'.join(map(re.escape, delimiters))
print(regexPattern)

entries = []
with open('data.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()

    for line in filecontents:
        line = line[:-1]  # remove newline at end of line
        args = re.split(regexPattern, line)
        entry = Entry(*args)
        entries.append(entry)

valid_passwords = 0

entry: Entry
for entry in entries:
    occurences = entry.password.count(entry.letter)
    is_valid = int(entry.minimum) <= occurences <= int(entry.maximum)
    if is_valid:
        print(entry)
        valid_passwords += 1

print("Valid passwords:", valid_passwords)
