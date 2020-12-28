import fileinput
import itertools
import numpy as np

numbers = [int(line) for line in fileinput.input()]

print([np.product(combo) for combo in itertools.combinations(numbers, 2) if sum(combo) == 2020])
print([np.product(combo) for combo in itertools.combinations(numbers, 3) if sum(combo) == 2020])

print(len(list(itertools.combinations(numbers, 3))))
print(200 * 199 * 198 / 6)

text = "LUCA"
new_text = [letter * 3 for letter in text]
new_text = ''.join(new_text)
print(new_text)

t1 = ['L', 'j', 'e', 'g', 'b']
t2 = ['ieve', 'ongens', 'ten', 'raag', 'rinta.']
text = ' '.join([''.join(word) for word in zip(t1, t2)])
text = text.replace('v', 'b')
text = text.replace('o', 'u')
print(text)