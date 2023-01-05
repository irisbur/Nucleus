from time import time


def compress(text):
    encoded = []
    i = 0
    dis_vec = []
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
            encoded.append(str(best_len))
            dis_vec.append(i - best_index)
        else:
            encoded.append(text[i])
            best_len = 0
        i += best_len if best_len else 1
    return encoded, dis_vec


def decompress(encoded, dis_vec):
    i = 0
    dis_index = 0
    decoded = []
    added = 0
    for i in range(len(encoded)):
        if len(encoded[i]) == 8:
            decoded += [encoded[i]]
        else:
            length = int(encoded[i])
            dis = dis_vec[dis_index]
            for j in range(length):
                decoded += [decoded[i + added - dis + j]]

            added += length - 1
            dis_index += 1
    return decoded

def lz_output(file_name):
    content = [f"{n:08b}" for n in open(file_name, "rb").read()]
    start = time()
    encoded, dis_vec = compress(content)
    print(time() - start)
    # print(content)
    # print(encoded, dis_vec)
    decoded = decompress(encoded, dis_vec)
    # print(decoded)
    print(decoded == content)

    return encoded, dis_vec


lz_output("Samp2    .bin")