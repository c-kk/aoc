import attr
import pprint


# Function to quickly split a string by multiple delimiters
def split(delimiters, string, maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)


# Read the data from the file
with open('data.txt', 'r') as file:
    data = file.read()

# Split string into passport chunks by empty line
chunks = data.split('\n\n')

# Split chunks into key-value fields by empty line or by space
kv_chunks = [split(["\n", " "], chunk) for chunk in chunks]
# print(*kv_chunks, sep='\n')

# Convert key-value chunks to passport dicts
passport_dicts = []
for kv_chunk in kv_chunks:
    passport_dict = {}
    for kv in kv_chunk:
        [key, value] = kv.split(':')
        passport_dict[key] = value
    passport_dicts.append(passport_dict)


# Convert passport dicts to passport objects
@attr.s
class Passport:
    byr = attr.ib(default=None)
    iyr = attr.ib(default=None)
    eyr = attr.ib(default=None)
    hgt = attr.ib(default=None)
    hcl = attr.ib(default=None)
    ecl = attr.ib(default=None)
    pid = attr.ib(default=None)
    cid = attr.ib(default="itdoesntmatter")


passports = []
for passport_dict in passport_dicts:
    passport = Passport(**passport_dict)
    passports.append(passport)

# print(passports)
# exit()

# Select the valid passports by filtering on the None value in the attributes
valid_passports = []
for passport in passports:
    values = passport.__dict__.values()
    is_valid = None not in values
    if is_valid:
        valid_passports.append(passport)

# Count the valid passports
pprint.pprint(valid_passports)
print("Count:", len(valid_passports))

# 245 - too high
# 208 - correct (** for kwargs!)
