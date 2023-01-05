import huffman
import full_lz


def deflate_compress(filename):

    lengths_and_text, dis_vec = full_lz.lz_output(filename)
    print("Items in first list: " + str(len(lengths_and_text)))
    huff_lengths, tree = huffman.compress(lengths_and_text)

    # todo: compress tree
    encoded_tree = None

    # todo: save as file
    f = open(filename + "_compressed.bin", "wb")
    # f.write()
    return huff_lengths, encoded_tree


def deflate_decompress(filename):
    pass


def main():
    deflate_compress("Samp1.bin")
    # print("Decoded Output", huffman.decompress(huff_lengths, tree))


if __name__ == '__main__':
    main()