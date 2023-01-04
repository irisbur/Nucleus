from time import time


def compress(text):
    encoded = []
    i = 0
    while i < len(text):
        best_len, best_index = 0, i
        for j in range(i - 1, -1, -1):
            k = 0
            while i + k < len(text) and text[i + k] == text[j + k]:
                k += 1
            if k > best_len:
                best_len = k
                best_index = j
        if best_len >= 4:
            encoded += [[best_len, i - best_index]]
        else:
            encoded += [text[i]]
            best_len = 0
        i += best_len + 1
    return encoded


def lz_output(file_name):
    content = [f"{n:08b}" for n in open(file_name, "rb").read()]
    start = time()
    encoded = compress(content)
    print(time() - start)
    dis_vec = []
    for i in range(len(encoded)):
        if len(encoded[i]) != 8:
            dis_vec.append(encoded[i][1])
            encoded[i] = str(encoded[i][0])
    return encoded, dis_vec