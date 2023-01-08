def compress(filename):
    text = [f"{n:08b}" for n in open(filename, "rb").read()]
    encoded = []
    i = 0
    dis_vec = []
    rows_dict = dict()
    while i < len(text):
        best_len, best_index = 0, i
        joined_bits = text[i]
        k = 1
        while i + k < len(text) and k < 255:
            joined_bits += text[i + k]
            if joined_bits in rows_dict:
                best_len = k
                best_index = rows_dict[joined_bits]
            else:
                rows_dict[joined_bits] = i
            k += 1

        if best_len >= 4:
            encoded.append(str(best_len))
            dis_vec.append(best_index)
        else:
            encoded.append(text[i])
            best_len = 0

        i += best_len if best_len else 1

    return encoded, dis_vec


def decompress(encoded, dis_vec):
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
                decoded += [decoded[dis + j]]
            added += length - 1
            dis_index += 1
    return decoded
