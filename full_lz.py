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


def decompress(encoded, dis_vec):
    i = 0
    dis_index = 0
    decoded = []
    for i in range(len(encoded)):
        if len(encoded[i]) == 8:
            decoded += [encoded[i]]
        else:
            length = int(encoded[i])
            dis = dis_vec[dis_index]
            for j in range(length):
                decoded += [decoded[i - dis + j]]
            dis_index += 1
        i += 1
    return decoded

def lz_output(file_name):
    content = [f"{n:08b}" for n in open(file_name, "rb").read()][:120]
    start = time()
    encoded = compress(content)
    print(time() - start)
    dis_vec = []
    for i in range(len(encoded)):
        if len(encoded[i]) != 8:
            dis_vec.append(encoded[i][1])
            encoded[i] = str(encoded[i][0])

    print(content)
    print(encoded, dis_vec)
    decoded = decompress(encoded, dis_vec)
    print(decoded)
    print(decoded == content)

    return encoded, dis_vec


lz_output("Samp1.bin")