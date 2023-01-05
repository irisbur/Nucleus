from math import log2


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


def compress_distances_vector_to_bits(dis_vec):
    bits_string = ""
    length = dem_to_bin(len(dis_vec))
    length = pad(length, 16)
    jumps = []
    max_dis = 2
    for i in range(len(dis_vec)):
        while dis_vec[i] >= max_dis:
            jumps.append(i)
            max_dis = 2 * max_dis if max_dis else 1
        dis = dem_to_bin(dis_vec[i])
        dis = pad(dis, int(log2(max_dis)))
        bits_string += dis
    jumps_in_16bits = "".join([pad(dem_to_bin(x), 16) for x in jumps])
    jumps_in_16bits = pad_from_right(jumps_in_16bits, 256)
    return length + jumps_in_16bits + bits_string


def de_compress_distances_vector_from_bits(bits):
    length = bin_to_dem(bits[:16])
    jumps = [bin_to_dem(bits[i: i + 16]) for i in range(16, 256 + 16, 16)]
    jumps = [jumps[i] for i in range(len(jumps)) if i == 0 or jumps[i] >= max(jumps[:i]) or jumps[i] > 0]
    max_dis = 2
    i = 0
    index = 256 + 16
    dis_vec = []
    while i < length:
        while jumps and i >= jumps[0]:
            max_dis = 2 * max_dis if max_dis else 1
            jumps = jumps[1:]
        dis_vec.append(bin_to_dem(bits[index: index + int(log2(max_dis))]))
        i += 1
        index += int(log2(max_dis))
    return dis_vec, length + 16


