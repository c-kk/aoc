def to_array(dct, gap_value):
	"""Convert dict (x,y): value to array [x][y] = value with default value for empty gaps"""
	xs, ys = [key[0] for key in dct], [key[1] for key in dct]
	xr, yr = range(min(xs), max(xs) + 1), range(min(ys), max(ys) + 1)
	arr = [[dct.get((x, y), gap_value) for x in xr] for y in yr]
	return arr

def to_string(dct, gap_value, chars):
	"""Convert dict (x,y): value to a multiline string for output.

	Example:
		dictxy.to_string(dct, gap_value=3, chars='#.O ')

    Args:
        dct: A dictionary with (x, y) pairs as key and a number as value. Numbers are in range [0, and up].
        gap_value: The value to be used for missing (x, y) pairs.
        chars: A lookup string to convert to the value to a character for output. 

    Returns:
        A multiline string
    """
	a = to_array(dct, gap_value)
	return '\n'.join(''.join(chars[x] for x in y) for y in a)