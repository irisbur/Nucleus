

def compress(filename):
    list_of_srings = [f"{n:08b}" for n in open(filename, "rb").read()]
    encoded = []
    i = 0
    dis_vec = []
    rows_dict = dict()
    while i < len(list_of_srings):
        best_len, best_index = 0, i
        joined_bits = list_of_srings[i]
        k = 1
        while i + k < len(list_of_srings) and k < 255:
            joined_bits += list_of_srings[i + k]
            if joined_bits in rows_dict:
                best_len = k + 1
                best_index = rows_dict[joined_bits]
            else:
                rows_dict[joined_bits] = i
            k += 1

        if best_len >= 4:
            encoded.append(str(best_len))
            dis_vec.append(best_index)
        else:
            encoded.append(list_of_srings[i])
            best_len = 0

        if best_len != 0:
            for index in range(i + 1, i + best_len):
                joined_bits = ""
                t = 0
                while index + t < len(list_of_srings) and t < 255:
                    joined_bits += list_of_srings[index + t]
                    if joined_bits not in rows_dict:
                        rows_dict[joined_bits] = index
                    t += 1

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
