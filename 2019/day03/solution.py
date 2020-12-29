# jonathan_paulson
# 38 points
# ·
# 1 year ago
# #2/#2! And now #2 on the overall leaderboard :)
# There's probably a more efficient solution,
# but using brute force makes this much easier.
# Video of me solving (and explaining the solution) at
# https://www.youtube.com/watch?v=tMPQp60q9GA

# A,B,_ = open('3.in').read().split('\n')

A, B = open("2019/day3/data.txt").read().split('\n')
A, B = [x.split(',') for x in [A, B]]

DX = {'L': -1, 'R': 1, 'U': 0, 'D': 0}
DY = {'L': 0, 'R': 0, 'U': 1, 'D': -1}
def get_points(A):
    x = 0
    y = 0
    length = 0
    ans = {}
    for cmd in A:
        d = cmd[0]
        n = int(cmd[1:])
        assert d in ['L', 'R', 'U', 'D']
        for _ in range(n):
            x += DX[d]
            y += DY[d]
            length += 1
            if (x, y) not in ans:
                ans[(x, y)] = length
    return ans

PA = get_points(A)
PB = get_points(B)
both = set(PA.keys()) & set(PB.keys())
part1 = min([abs(x) + abs(y) for (x, y) in both])
part2 = min([PA[p] + PB[p] for p in both])
print(part1, part2)

pass
# level 2
# mcpower_
# 26 points
# ·
# 1 year ago
# Some useful Python speed-coding things:
#
# line 1: str.splitlines strips any terminal linebreaks, which is probably what you want (and avoids the extra _ destructuring). Alternatively, str.split without any arguments splits on any whitespace and essentially strips leading/trailing whitespace. Therefore, you can replace this with A,B = open('3.in').read().splitlines() or A,B = open('3.in').read().split() (as the only whitespace in the input are new lines). Could also str.strip before splitting!
#
# line 1: open() is iterable of lines (with the new line character), so you can do A,B = list(map(str.rstrip, open('3.in'))) as well
#
# line 14: strings are iterable, so you can do assert d in 'LRUD'
#
# lines 4, 5: writing a dict manually is a bit annoying, so you can take advantage of the constructor of an iterable of pairs like so:
#
#   DX = dict(zip('LRUD', [-1,1,0,0]))
#   DY = dict(zip('LRUD', [0,0,1,-1]))
# lines 26, 27: for most functions which take in lists (filter, map, min, max, sum, etc.), you can use a generator expression instead of a list comprehension, saving two characters of typing:
#
#   part1 = min(abs(x)+abs(y) for x,y in both)
#   part2 = min(PA[p]+PB[p] for p in both)
# (you also don't need the parens for destructuring a tuple!)
