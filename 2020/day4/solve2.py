import attr
import cerberus
import re

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
schunks = [chunk.split('\n') for chunk in chunks]
print(*schunks, sep='\n')
exit()

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


# Validate passports
class MyValidator(cerberus.Validator):
    def _validate_isbyr(self, isset, field, val):
        try:
            if not 1920 <= int(val) <= 2002: raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_isiyr(self, isset, field, val):
        try:
            if not 2010 <= int(val) <= 2020: raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_iseyr(self, isset, field, val):
        try:
            if not 2020 <= int(val) <= 2030: raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_ishgt(self, isset, field, val):
        try:
            if "cm" in val:
                height = int(val.replace('cm', ''))
                if not 150 <= height <= 193: raise
            elif "in" in val:
                height = int(val.replace('in', ''))
                if not 59 <= height <= 76: raise
            else:
                raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_ishcl(self, isset, field, val):
        try:
            if not re.search(r'#[a-fA-F0-9]{6}$', val):
                raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_isecl(self, isset, field, val):
        try:
            if val not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                raise
        except:
            self._error(field, field + " " + str(val) + " is invalid")

    def _validate_ispid(self, isset, field, val):
        try:
            if not len(val) == 9:
                raise
            val = int(val)
        except:
            self._error(field, field + " " + str(val) + " is invalid")


schema = {
    'byr': {'isbyr': True},
    'iyr': {'isiyr': True},
    'eyr': {'iseyr': True},
    'hgt': {'ishgt': True},
    'hcl': {'ishcl': True},
    'ecl': {'isecl': True},
    'pid': {'ispid': True},
    'cid': {},
}
v = MyValidator(schema)


valid_passports = []
for passport in passports:
    passport_dict = passport.__dict__
    is_valid = v.validate(passport_dict)
    if is_valid:
        valid_passports.append(passport)
    else:
        print(v.errors)

print("Count:", len(valid_passports))
# 167 - Correct!