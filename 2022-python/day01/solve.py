lines = open("data.txt").read().split('\n')
numbers = [int(float(number + '.0')) for number in lines]

highest = 0
current = 0

for num in numbers:
    print('num', num, 'current', current, 'highest', highest)

    if num > 0:
        current += num
    else:
        highest = max(highest, current)
        current = 0

print(highest)

no1 = 0
no2 = 0
no3 = 0
current = 0
total = 0

for num in numbers:
    print('num', num, 'current', current, 'no1', no1, 'no2', no2, 'no3', no3, 'total', total)

    if num > 0:
        current += num
    else:
        if current > no1:
            no3 = no2
            no2 = no1
            no1 = current
        elif current > no2:
            no3 = no2
            no2 = current
        elif current > no3:
            no3 = current

        total = no1 + no2 + no3
        current = 0

print(total)
