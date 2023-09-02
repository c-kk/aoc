import time 
import numpy as np

def list_to_int(lst):
    integer = 0
    for i, num in enumerate(reversed(lst)):
        integer += num << (8 * i)
    return integer

def int_to_list(integer):
    lst = []
    for _ in range(4):
        lst.append(integer & 255)
        integer >>= 8
    return list(reversed(lst))

def add_lists_regular(lst1, lst2):
    return lst1 + lst2
    # return [a + b for a, b in zip(lst1, lst2)]

print('Comparing bitshift vs regular addition for 4-element lists (1.000.000 times)')

list1 = [0, 1, 4, 8]
list2 = [3, 4, 7, 4]

int1 = list_to_int(list1)
int2 = list_to_int(list2)

start_time_bitshift = time.time()
for _ in range(1000000):
    sum_int = int1 + int2
end_time_bitshift = time.time()

list1_np = np.array(list1)
list2_np = np.array(list2)

start_time_regular = time.time()
for _ in range(1000000):
    result_list = add_lists_regular(list1_np, list2_np)
end_time_regular = time.time()

time_bitshift = end_time_bitshift - start_time_bitshift
time_regular = end_time_regular - start_time_regular

print(f"Bitshift: {time_bitshift}")
print(f"Regular: {time_regular}")

# Setting and getting the nth number from a bit-shifted integer
def get_nth_number(integer, n):
    """Retrieve the nth number from the bit-shifted integer."""
    return (integer >> (8 * n)) & 255

def set_nth_number(integer, n, value):
    """Set the nth number in the bit-shifted integer."""
    # Clear the nth byte
    integer &= ~(255 << (8 * n))
    # Set the new value
    integer |= (value << (8 * n))
    return integer

# Test the functions
test_integer = list_to_int([0, 1, 4, 8])

# Retrieve the 2nd number (0-indexed)
retrieved_value = get_nth_number(test_integer, 2)

# Set the 2nd number to 7
updated_integer = set_nth_number(test_integer, 2, 7)
updated_list = int_to_list(updated_integer)

print(retrieved_value, updated_list)
