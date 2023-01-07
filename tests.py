
import huffman
import compress_tree


def test_decompress():
    data = [*"asdjafdkasjdfhaskfjdlfkgfegkegekfgbvasekvasvdslkfsfldkxmdrpes"]
    encoded_output, huff_dict = huffman.compress(data)
    decoded_output = huffman.decompress(encoded_output, huff_dict)

    print(decoded_output == "asdjafdkasjdfhaskfjdlfkgfegkegekfgbvasekvasvdslkfsfldkxmdrpes")
    # return are_trees_equal(tree, decomp_tree)

if __name__ == '__main__':
    print(test_decompress())