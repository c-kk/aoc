# Examples
# Transform 7 with loop 8 = 5764801
# ckey = 5764801
# clop = 8

# Transform 7 with loop 11 = 17807724
# dkey = 17807724
# dlop = 11

# Transform 17807724 with loop 8 = 14897079
# dkey = 17807724
# clop = 8
# ekey = 14897079

# Transform 5764801 with loop 11 = 14897079
# ckey = 5764801
# dlop = 11
# ekey = 14897079

# Calculate loops
dkey = 5293040
value = 1
for loop1 in range(1, 20201227):
	value = (value * 7) % 20201227
	if value == dkey: break

# Calculate encryption key
ckey = 8184785
ekey = 1
for loop2 in range(0, loop1):
	ekey = (ekey * ckey) % 20201227

print('Encryption key:', ekey)