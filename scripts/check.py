# Prints a dictionary of the count of each character in the given string
# No comparison is performed, must be checked by eye. Or just implement the
# comparison, whatever is easier ¯\_(ツ)_/¯
from collections import OrderedDict


def check(s):
    od = OrderedDict()
    for c in s:
        if c not in od:
            od[c] = 1
        else:
            od[c] += 1
    return od


def main():
    s1 = "80f82fc0e320fe3e2aba1e15644ee6d5622a5f463f7145dd0b74caa3898e9f0f"
    s2 = "83538ab1c15f7a89050be8dbdf7f99cfc31cf501bbf4625992e067391f44599f"

    chars1 = check(s1)
    chars2 = check(s2)

    print(chars1)
    print(chars2)


if __name__ == "__main__":
    main()
