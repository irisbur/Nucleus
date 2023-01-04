

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



codes = dict()


def Calculate_Codes(node, val=''):
    """
    A helper function to print the codes of symbols by traveling Huffman Tree
    """
    # huffman code for current node
    new_val = val + str(node.code)

    if node.left:
        Calculate_Codes(node.left, new_val)
    if node.right:
        Calculate_Codes(node.right, new_val)

    if not node.left and not node.right:
        codes[node.symbol] = new_val

    return codes


""" A helper function to obtain the encoded output"""


def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        #  print(coding[c], end = '')
        encoding_output.append(coding[c])

    string = ''.join([str(item) for item in encoding_output])
    return string


""" A helper function to calculate the space difference between compressed and non compressed data"""


def Total_Gain(data, coding):
    before_compression = len(data) * 8  # total bit space to stor the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])  # calculate how many bit is required for that symbol in total
    print("Space usage before compression (in bits):", before_compression)
    print("Space usage after compression (in bits):", after_compression)


def huffman_encoding(data):
    symbol_with_probs = count_frequencies(data)
    symbols = symbol_with_probs.keys()
    probabilities = symbol_with_probs.values()
    print("symbols: ", symbols)
    print("probabilities: ", probabilities)

    nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)
        # for node in nodes:
        #      print(node.symbol, node.prob)

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

    huffman_encoding = Calculate_Codes(nodes[0])
    print("symbols with codes", huffman_encoding)
    Total_Gain(data, huffman_encoding)
    encoded_output = Output_Encoded(data, huffman_encoding)
    return encoded_output, nodes[0]


def Huffman_Decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol is None and huffman_tree.right.symbol is None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = ''.join([str(item) for item in decoded_output])
    return string


""" First Test """
initial_data = open('compressed.txt', 'r').read().split(', ')
data = [s[1:-1] for s in initial_data]
print(len(data))
# print(data)
encoding, tree = huffman_encoding(data)
print("Encoded output", encoding)
# print("Decoded Output", Huffman_Decoding(encoding, tree))

""" Second Test """

# f = open("demofile.txt", "r")

# data = f.read()
# print(data)
# Huffman_Encoding(data)
