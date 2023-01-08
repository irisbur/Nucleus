

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right

        # tree direction (0/1)
        self.code = ''


def count_frequencies(words):
    """
    A helper function to calculate the probabilities of symbols in given data.
    """
    code_book = dict()
    for word in words:
        if word in code_book.keys():
            code_book[word] += 1
        else:
            code_book[word] = 1
    return code_book


def calculate_codes(node, codes, val=''):
    """
    A helper function to print the codes of symbols by traveling Huffman Tree
    """
    # huffman code for current node
    new_val = val + str(node.code)

    if node.left:
        calculate_codes(node.left, codes, new_val)
    if node.right:
        calculate_codes(node.right, codes, new_val)

    if not node.left and not node.right:
        codes[node.symbol] = new_val

    return codes


def encode_data(data, coding):
    encoding_output = ''
    for c in data:
        encoding_output += coding[c]
    return encoding_output


def compress(data):
    symbol_with_probs = count_frequencies(data)
    symbols = symbol_with_probs.keys()

    nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)

        # pick 2 smallest nodes
        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        # combine the 2 smallest nodes to create new node
        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    huffman_encoding = calculate_codes(nodes[0], dict())
    encoded_output = encode_data(data, huffman_encoding)
    return encoded_output, huffman_encoding


def decompress(encoded_data, huffman_dict):
    value_word_dict = {v: k for k, v in huffman_dict.items()}

    decoded_data = []
    i = 0
    while len(encoded_data) > 1:
        if encoded_data[:i] in value_word_dict.keys():
            decoded_data.append(value_word_dict[encoded_data[:i]])
            encoded_data = encoded_data[i:]
            i = 0
        else:
            i += 1

    return decoded_data

