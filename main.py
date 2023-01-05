import huffman
import full_lz
from bitarray import bitarray
import compress_distances_vector

DIST_BITS_NUM = 16
HUFF_DICT_BITS_SIZE = 16
PADDING_BITS_NUM_SIZE = 8


def deflate_compress(filename):
    lengths_and_text, dis_vec = full_lz.lz_output(filename)
    print("Items in first list: " + str(len(lengths_and_text)))
    huff_lengths, huffman_encoding = huffman.compress(lengths_and_text)
    encoded_dist = compress_distances_vector.compress_distances_vector_to_bits(dis_vec)
    # todo: compress tree
    encoded_huff_dict = None  # returns bits that represents the tree

    all_compressed_data = encoded_dist + encoded_huff_dict + huff_lengths
    num_zeros_to_pad = len(all_compressed_data) % 8
    len_pad_byte = compress_distances_vector.pad(num_zeros_to_pad, 8)
    # save to binary file.
    f = open(filename + "_compressed.bin", "wb")
    f.write(bitarray(len_pad_byte + num_zeros_to_pad + all_compressed_data))
    f.close()


def deflate_decompress(filename):
    # todo: de-comp dist-tree-huff
    f = open(filename, "rb")
    bytes_data = ''.join([f"{n:08b}" for n in f.read()])

    # how many zeros added? 0-8
    pad_num = int(bytes_data[:PADDING_BITS_NUM_SIZE], 2)
    bytes_data = bytes_data[PADDING_BITS_NUM_SIZE + pad_num:]

    # get distances vector for lz
    dist_size = int(bytes_data[:DIST_BITS_NUM], 2)
    encoded_dists = bytes_data[DIST_BITS_NUM: DIST_BITS_NUM + dist_size]
    decoded_dists = compress_distances_vector.de_compress_distances_vector_from_bits(encoded_dists)

    # crop out used data
    bytes_data = bytes_data[DIST_BITS_NUM + dist_size:]

    # get huff code book
    dict_size = int(bytes_data[:HUFF_DICT_BITS_SIZE])
    encoded_huff_dict = bytes_data[HUFF_DICT_BITS_SIZE: HUFF_DICT_BITS_SIZE + dict_size]
    decoded_huff_dict = None  # decode(encoded_huff_dict) # todo: decode dict :)
    # crop out used data
    bytes_data = bytes_data[HUFF_DICT_BITS_SIZE + dict_size:]

    # decode text & lengths using huffman
    decoded_huff_text = huffman.decompress(bytes_data, decoded_huff_dict)

    # decode to lz
    data = full_lz.decompress(decoded_huff_text, decoded_dists)
    f = open(filename + "_decompressed.bin", 'wb')
    f.write(data)
    f.close()


def main():
    # f = open("Samp1.bin", "wb")
    full_lz.lz_output("Samp1.bin")
    # f.close()
    # deflate_decompress("demofile.bin")


if __name__ == '__main__':
    main()