import huffman
import full_lz
from bitarray import bitarray
import compress_distances_vector
import compress_tree
from time import time


DIST_BITS_NUM = 16
HUFF_DICT_BITS_SIZE = 16
PADDING_BITS_NUM_SIZE = 8


def deflate_compress(filename):
    # start = time()
    lengths_and_text, dis_vec = full_lz.compress(filename)

    huff_output, huffman_encoding = huffman.compress(lengths_and_text)
    encoded_dist = compress_distances_vector.compress_distances_vector_to_bits(dis_vec)

    encoded_huff_dict = compress_tree.compress_tree(huffman_encoding)  # returns bits that represents the tree

    all_compressed_data = encoded_dist + encoded_huff_dict + huff_output
    num_zeros_to_pad = (8 - len(all_compressed_data) % 8) * '0' if (8 - len(all_compressed_data) % 8) != 8 else ''
    len_pad_byte = compress_distances_vector.pad(
        compress_distances_vector.dem_to_bin(len(num_zeros_to_pad)), 8
    )
    # print("comp time", time() - start)
    # save to binary file.
    f = open(filename[:-4] + "_compressed.bin", "wb")
    print("compressed file size: " + str(len(len_pad_byte + num_zeros_to_pad + all_compressed_data)/8))
    f.write(bitarray(len_pad_byte + num_zeros_to_pad + all_compressed_data))
    f.close()


def deflate_decompress(filename):
    f = open(filename, "rb")
    bytes_data = ''.join([f"{n:08b}" for n in f.read()])

    # how many zeros added? 0-8
    pad_num = int(bytes_data[:PADDING_BITS_NUM_SIZE], 2)
    bytes_data = bytes_data[PADDING_BITS_NUM_SIZE + pad_num:]

    # get distances vector for lz
    decoded_dists, bits_taken = compress_distances_vector.de_compress_distances_vector_from_bits(bytes_data)

    # crop out used data
    bytes_data = bytes_data[bits_taken:]

    # get huff code book
    decoded_huff_dict, bits_taken = compress_tree.de_compress_tree(bytes_data)
    # crop out used data
    bytes_data = bytes_data[bits_taken:]

    # decode text & lengths using huffman
    decoded_huff_text = huffman.decompress(bytes_data, decoded_huff_dict)

    # decode to lz
    data = full_lz.decompress(decoded_huff_text, decoded_dists)

    byte_data = [int(bits8, 2).to_bytes(1, byteorder='big') for bits8 in data]

    f = open(filename[:-4] + "_decompressed.bin", 'wb')

    f.write(b''.join(byte_data))
    f.close()


def main():
    for i in range(1, 5):
        deflate_compress(f"Samp{i}.bin")
        deflate_decompress(f"Samp{i}_compressed.bin")
    # huff_compress("Samp1.bin")


if __name__ == '__main__':
    main()
