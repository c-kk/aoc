from operator import mul, add
import argparse
from pathlib import Path


OPER = {1: add, 2: mul}


def calc(X):
    L = list(X)
    idx = 0
    op = L[idx]
    while op != 99:
        v1 = L[L[idx + 1]]
        v2 = L[L[idx + 2]]
        i = L[idx + 3]
        L[i] = OPER.get(op)(v1, v2)
        idx += 4
        op = L[idx]
        print(idx, L)
    return L


def main(parser, args):
    if Path(args.input).is_file():
        with open(args.input, "r") as fh:
            modules = [[int(i) for i in l.strip().split(",")] for l in fh]
    else:
        parser.error("input is not a file")

    if args.part == "1":
        print("Part 01")
        for i in modules:
            i[1] = args.a
            i[2] = args.b
            print(calc(i)[0])
    elif args.part == "2":
        print("Part 02")
        for i in modules:
            for j in range(*args.a):
                for k in range(*args.b):
                    i[1] = j
                    i[2] = k
                    x = calc(i)[0]
                    if x == args.t:
                        print(f"100 * {j} + {k} = {100 * j + k}")
                        break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    s = parser.add_subparsers(dest="part")

    p1 = s.add_parser("1")
    p1.add_argument("input")
    p1.add_argument("a", type=int)
    p1.add_argument("b", type=int)

    p2 = s.add_parser("2")
    p2.add_argument("input")
    p2.add_argument("a", type=int, nargs=2)
    p2.add_argument("b", type=int, nargs=2)
    p2.add_argument("t", type=int)
    main(parser, parser.parse_args())