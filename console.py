import math


# 0100110010001101000001111010101100110000011001011110100111100011001011110111110001100100011011000110001100101010011001110000100010111101001110001010100111101001110010000111010101100000011011111000111100101110000011000110101011101001110010001010110101101000110011111010100001100111111000010101010010001001101111010110001100100011111000101000110001010011101110001001100100011010000011110101011001100000110010111101001111000110010111101111100011001000110110001100011001010100110011100001000101111010011100010101001111010011100100001110101011000000110111110001111001011100000110001101010111010011100100010101101011010001100111110101000011001111110000101010100100010011011110101100011001000111110001010001100010100111011100010011001000110100000111101010110011000001100101111010011110001100101111011111000110010001101100011000110010101001100111000010001011110100111000101010011110100111001000011101010110000001101111100011110010111000001100011010101110100111001000101011010110100011001111101010000110011111100001010101001000100110


def xor(a):
    res = 0
    for i in a:
        res ^= i
    return res


def prod(a):
    res = 1
    for i in a:
        res *= i
    return res


def valid_eval(f):
    f = str(f)
    if all([(lambda x: str(x) == "1" or str(x) == "0")(x) for x in f]) and math.log2(len(f)).is_integer():
        return True
    else:
        return False


def truth_table(f):
    f = str(f)
    cols = math.ceil(math.log2(len(f)))
    rows = len(f)
    table = []
    for i in range(rows):
        v = [int(r) for r in bin(i)[2:].zfill(cols)]
        dirty_row = [j for j in list(zip([v], [[int(f[i])]]))][0]
        r = []
        for item in dirty_row:
            r.extend(item)
        table.append(r)
    return table


def is_P0(eval):
    return eval[0] == "0"


def is_P1(eval):
    return eval[-1] == "1"


def is_L(eval):
    table_orig = truth_table(eval)
    table = [[]]
    for i in table_orig:
        if i[:-1].count(1) == 1:
            table.append(i)
    table = table[1:]
    a = [0] * (len(table[0][:-1]) + 1)
    a[0] = table_orig[0][-1]
    for i in range(0, len(table[0][:-1])):
        a[len(table[0][:-1]) - i] = a[0] ^ table[i][-1]
    new_eval = [a[0]] * len(eval)
    for i in range(1, len(table_orig)):
        for j in range(len(table_orig[i][:-1])):
            new_eval[i] ^= table_orig[i][j] * a[j + 1]
    eval = str(eval)
    str_new_eval = ""
    for i in new_eval:
        str_new_eval += str(i)
    new_eval = str_new_eval
    if new_eval == eval:
        return True
    else:
        return False


def is_S(eval):
    new_eval = str(eval[::-1]).replace("1", "*").replace("0", "1").replace("*", "0")
    if eval == new_eval:
        return True
    else:
        return False


def is_M(eval):
    eval = str(eval)
    table = truth_table(eval)
    if "1" in eval:
        starter = eval.index("1")
    else:
        starter = 0
    table = table[starter:]
    for i in range(len(table)):
        for j in range(i + 1, len(table)):
            checker = [x <= y for x in table[i][:-1] for y in table[j][:-1]]
            if all(checker):
                comparable = True
            else:
                comparable = False
            if comparable:
                if table[i][-1] > table[j][-1]:
                    return False
    return True


f_eval = str(input("Введите eval функции: "))
t = truth_table(f_eval)
for i in t:
    print(*i)
print("P0: ", is_P0(f_eval))
print("P1: ", is_P1(f_eval))
print("L:  ", is_L(f_eval))
print("S:  ", is_S(f_eval))
print("M:  ", is_M(f_eval))
