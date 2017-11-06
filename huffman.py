#Name: Mani Movva
#Section: 07

#A HuffmanNode is a class
# A HuffmanNode is a node that contains a character and the frequency of that character
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # the character oode
        self.freq = freq  # freq is an int representing the number of times the character appears in the original text
        self.code = None  # code is a string of the binary sequence that represents the character
        self.left = None  # left and right are HuffmanNodes that this node points to 
        self.right = None

    #boiler plate
    def __repr__ (self):
        return " %s %s" % (chr(self.char), self.freq)

    def __eq__(self, other):
        return ((type(other) == HuffmanNode)
            and self.char == other.char
            and self.freq == other.freq)

# HuffmanNode, HuffmanNode -> Boolean
def comes_before (a, b) :
    """returns a boolean representing if a comes before b, it takes HuffmanNodes a and b as input parameters"""
    if a.freq == b.freq:
        if a.char < b.char:               # comparing which char comes first
            return True
        return False
    elif a.freq < b.freq:
        return True
    return False

# filename -> list of integers
def cnt_freq(filename):
    """returns a list of the frequencies of each character, takes a text file as a parameter"""
    freqList = [0]*256
    try:
        file = open(filename,encoding='utf-8-sig')
    except:
        raise IOError("Input file not found")
    text = file.read()
    file.close()
    for i in range(len(text)):
        freqList[ord(text[i])] += 1
    return freqList                     # list of frequencies of each character
   
# list of integers -> HuffmanNode
def create_huff_tree(char_freq_list):
    """returns a single HuffmanNode with pointers to the rest of the nodes, takes a list of character frequencies as an input"""
    nodeList = []                       # list of nodes
    currentIndex = 0
    for i in range(len(char_freq_list) ):
        if char_freq_list[i] > 0:
            addingNode = HuffmanNode(i, char_freq_list[i])
            nodeList.append(addingNode) 
            currentIndex += 1
            # makes a list of Nodes with the character & frequency of that character

    root = combine(nodeList)
    return root[0]

# list of HuffmanNodes -> list of HuffmanNodes (with just one index
def combine(nodeList):
    """returns a single HuffmanNode with pointers to the rest of the nodes, takes a list of HuffmanNodes as an input"""
    while len(nodeList) != 1:  
        mins = findMin(nodeList)
        
        if mins[0].char < mins[1].char:
            newParentNode = HuffmanNode(mins[0].char, mins[0].freq+mins[1].freq)        # create a parent node
        else:
            newParentNode = HuffmanNode(mins[1].char, mins[0].freq+mins[1].freq)
        newParentNode.left = mins[0]                                        # make the two mins the child nodes
        newParentNode.right = mins[1]
        nodeList.remove(mins[0])                                            # remove the mins from the nodeList
        nodeList.remove(mins[1])            
        nodeList.append(newParentNode)                                      # add the new parent node to the nodeList
        root = combine(nodeList)                                            # recurse
    return nodeList

# list of HuffmanNodes -> tuple of HuffmanNodes    
def findMin(nodeList):
    """returns a tuple of the two minimum HuffmanNodes. Takes a list of nodes as input"""
    currentMin = nodeList[0]
    minIndex = 0
    for i in range(len(nodeList)):
        if comes_before(nodeList[i], currentMin):
            currentMin = nodeList[i]
            minIndex = i
    del (nodeList[minIndex])
    secondMin = nodeList[0]
    for i in range(len(nodeList)):
        if nodeList[i] != currentMin:
            if comes_before(nodeList[i], secondMin):
                secondMin = nodeList[i]
    nodeList.insert(minIndex, currentMin)
    return [currentMin, secondMin]

# HuffmanNode, string -> list of strings
def create_code(root_node, code = None, codeList = ['']*256):
    """returns a list of codes for respective ASCII values, takes a HuffmanNode as input"""
    if code is None:
        code = ''
    string0 = "0"
    string1 = "1"
    
    if root_node.left is not None:
        create_code(root_node.left, code+string0)
    
    if root_node.left is None and root_node.right is None:
        codeList[root_node.char] = code
        root_node.code = code
                
    if root_node.right is not None:
        create_code(root_node.right, code+string1)

    return codeList

# textfile, textfile -> textfile
def huffman_encode(in_file, out_file):
    """returns a textfile with an encoded message, requires an input textfile"""
    freqlist = cnt_freq(in_file)
    root_node = create_huff_tree(freqlist)
    codeList = create_code(root_node)
    codedString = ""
    
    if root_node.left is None and root_node.right is None:
        codedString = "%s %s" % (chr(root_node.char), root_node.freq)
        outputFile = open(out_file,'w+')
        outputFile.write(codedString)
        outputFile.close()

    
    try:                                                    # test for empty input file
        inputFile = open(in_file,encoding='utf-8-sig') 
    except:
        raise IOError("Input file not found")
        
    inputFileText = inputFile.read()
    inputFile.close()
    for i in range(len(inputFileText)):
        codedString += "%s"%codeList[ord(inputFileText[i])]

    outputFile = open(out_file,'w+')
    outputFile.write(codedString)
    outputFile.close()

    return out_file

# textfile, textfile -> textfile
def huffman_decode(freqs, encoded_file, decode_file):
    """returns a textfile with a decoded message, requires an input textfile"""
    root_node = create_huff_tree(freqs)

    try:                                                    # test for empty input file
        file = open(encoded_file,encoding='utf-8-sig') 
    except:
        raise IOError("Input file not found")

    text = file.read()
    file.close()
    current_node = root_node
    return_string = ""

    for i in range(len(text)):
        if text[i] == '0':
            current_node = current_node.left
        elif text[i] == '1':
            current_node = current_node.right
        if current_node.left is None and current_node.right is None:
            return_string += chr(current_node.char)
            current_node = root_node
            
    outputFile = open(decode_file,'w+')
    outputFile.write(return_string)
    outputFile.close()
    return decode_file

# HuffmanNode, string -> string
def tree_preord(node, return_string = None):
    """returns a string representing the contents of the HuffmanTree in preorder"""
    if return_string is None:
        return_string = ""
    if node is None:
        return return_string
    if node.left is not None or node.right is not None:
        return_string += "0"
    else:
        return_string += ("%s%s" % (chr(node.char), node.freq))
    return_string += tree_preord(node.left)
    return_string += tree_preord(node.right)
    return return_string


