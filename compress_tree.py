
KEY_EXTENDED_LEN = 9

LENGTH_LEN = 16

JUMPS_BIT = 16


def pad(num, to_bits_num):
    if len(num) < to_bits_num:
        return "0" * (to_bits_num - len(num)) + num
    return num


def pad_from_right(num, to_bits_num):
    if len(num) < to_bits_num:
        return num + "0" * (to_bits_num - len(num))
    return num


def dem_to_bin(ip_val):
    if ip_val >= 1:
        return dem_to_bin(ip_val // 2) + str(ip_val % 2)
    return ''


def bin_to_dem(bin_num):
    return int(bin_num, 2)


def sort_by_value_length(dictionary):
    sorted_list = sorted(dictionary, key=lambda item: len(dictionary[item]))
    l = []
    for k in sorted_list:
        if len(k) == 8:
            l.append(["0" + k, dictionary[k]])
        else:
            l.append(["1" + pad(dem_to_bin(int(k)), 8), dictionary[k]])
    return l


def compress_tree(dict_tree):
    sort_by_val = sort_by_value_length(dict_tree)
    bits_string = ""
    length = dem_to_bin(len(dict_tree))
    length = pad(length, 16)

    jumps = []
    key_len = 1
    for i in range(len(sort_by_val)):
        while len(sort_by_val[i][1]) > key_len:
            jumps.append(i)
            key_len += 1
        bits_string += sort_by_val[i][0] + sort_by_val[i][1]

    jumps_in_10bits = "".join([pad(dem_to_bin(x), JUMPS_BIT) for x in jumps])
    jumps_in_10bits = pad_from_right(jumps_in_10bits, JUMPS_BIT * JUMPS_BIT)
    return length + jumps_in_10bits + bits_string


def de_compress_tree(bits):
    length = bin_to_dem(bits[:LENGTH_LEN])
    jumps = [bin_to_dem(bits[i: i + JUMPS_BIT]) for i in range(LENGTH_LEN, JUMPS_BIT * JUMPS_BIT + LENGTH_LEN, JUMPS_BIT)]
    jumps = [jumps[i] for i in range(len(jumps)) if i == 0 or jumps[i] >= max(jumps[:i]) or jumps[i] > 0]
    key_len = 1
    i = 0
    index = JUMPS_BIT * JUMPS_BIT + LENGTH_LEN
    tree_dict = {}

    while i < length:
        while jumps and i >= jumps[0]:
            key_len += 1
            jumps = jumps[1:]

        key = bits[index: index + KEY_EXTENDED_LEN]
        if key[0] == '0':
            key = key[1:]
        else:
            key = str(bin_to_dem(key[1:]))

        word = bits[index + KEY_EXTENDED_LEN: index + KEY_EXTENDED_LEN + key_len]
        tree_dict[key] = word
        i += 1
        index += KEY_EXTENDED_LEN + key_len
    return tree_dict, index
