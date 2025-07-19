from enum import Enum, auto

class Nade:

    def __init__(self, name,value=0):
        self.name = name
        self.left = None
        self.right = None
        self.value = value
        self.parent = None
        #left is 0 and right is 1
    def print_out(self):
        print("Name:", self.name, "Left:", self.left, "Right:", self.right, "Value:", self.value)
    def pertinent_info(self):
        print(self.name,"-", self.value)
    
    def retrace_steps(self, retrace_path = None):
        
        if retrace_path == None: retrace_path = []
        if self.parent == None: return retrace_path #this is our termination point

        parent_node = self.parent
        if parent_node.right is self: retrace_path.append("1")
        if parent_node.left is self: retrace_path.append("0")
        return parent_node.retrace_steps(retrace_path)

class Deflate:

    class State(Enum):
        UNENCODED = auto()
        LZ77ENCODED = auto()
        HUFFMANENCODED = auto()

    def __init__(self,input_string):
        self.encoded_string = ""
        self.unencoded_string = input_string
        self.current_list = []
        self.huffman_tree = None
        self.status = Deflate.State.UNENCODED
        self.nade_list = []
        self.huffman_codes = dict()
    
    @staticmethod
    def string_match_up(string1,string2):
        best_match_length = 0
        for i in range(min(len(string1),len(string2))):
            if string2[i] == string1[i]: best_match_length += 1
            else: break
        return best_match_length
    
    @staticmethod
    def find_largest_string(search_buffer,lookahead_buffer):
        best_match_distance = 0
        best_match_length = 0
        biggest_chunk = ""

    
        current_match_length = 0
        for i in range(len(search_buffer)):
            current_match_length = Deflate.string_match_up(search_buffer[i:],lookahead_buffer)
            if current_match_length >= best_match_length:
                best_match_length = current_match_length
                best_match_distance = len(search_buffer) - i
                biggest_chunk = lookahead_buffer[:current_match_length]
    
        return best_match_distance,best_match_length,biggest_chunk

    def LZ77_encoding(self):
        search_buffer = ""
        lookahead_buffer = self.unencoded_string

        search_buffer_list = []

        while len(lookahead_buffer) > 0:
            distance,match_length,target_chunk = Deflate.find_largest_string(search_buffer,lookahead_buffer)
            
            if match_length == 0: match_length+=1
            
            search_buffer+=lookahead_buffer[:match_length]

            if match_length <= 2:search_buffer_list.append(lookahead_buffer[:match_length])
            else:
                search_buffer_list.append(254 + match_length)
                search_buffer_list.append(distance - 1)
            
            lookahead_buffer = lookahead_buffer[match_length:]


        for i in range(len(search_buffer_list)):
            if type(search_buffer_list[i]) == str: self.current_list.extend(list(search_buffer_list[i].encode('utf-8')))
            else: self.current_list.append(search_buffer_list[i])
        
        self.status = Deflate.State.LZ77ENCODED
    
    #determines the frequency of the numbers and creates nades list with probabilities
    def huffman_probabilities(self):
        huffman_frequency = dict()
        self.current_list.append(256) #EOD token
        for i in self.current_list:
            if i in huffman_frequency:
                huffman_frequency[i] += 1
            else:
                huffman_frequency[i] = 1
        
        # Create a list of Nade objects with their probabilities
        nades = []
        for char, freq in huffman_frequency.items():
            nades.append(Nade(name=char, value=freq))
        self.nade_list = nades
    
    def create_huffman_tree(self):
        #this takes in a list of Nade objects and builds a binary huffman tree
        self.nade_list.sort(key=lambda x: x.value)

        while len(self.nade_list) > 1:
            left = self.nade_list.pop(0)
            right = self.nade_list.pop(0)
            new_node = Nade(name=left.name + right.name,  value=left.value + right.value)
            new_node.left = left
            new_node.right = right
            left.parent = new_node
            right.parent = new_node
            self.nade_list.append(new_node)
            self.nade_list.sort(key=lambda x: x.value)
        self.huffman_tree = self.nade_list[0]
    
    def transform_to_huffman_codes(self):
        self.huffman_codes
        queue = []
        visited = []
        queue.append(self.huffman_tree)
        while len(queue) > 0:
            current_nade = queue.pop(0)
            current_nade.left.append()
            current_nade.right.append()
    
    def encode_LZ77_to_huffman(self):
        pass

# This function takes in the string representation of a binary number (no 0b prefix) and converts it into a list of bytes.

    def byte_manager(self,binary_number):
        byte_list = []
        
        binary_number_before_modification = binary_number
        length_true = len(binary_number_before_modification)
        leftover_length = len(binary_number) % 8
        
        leftover_bits = ""
        if leftover_length != 0: 
            leftover_bits = binary_number[-leftover_length:]
            binary_number = binary_number[:-leftover_length] # Remove leftover bits from the main binary string
        
        for i in range(int(len(binary_number)/8)):
            byte_list.append(int(binary_number[i*8:i*8 + 8],2))
        
        if len(leftover_bits) > 0:
            leftover_bits += "0" * (8 - leftover_length) #pad the leftover bits to make a full byte
            byte_list.append(int(leftover_bits,2))
        return byte_list

        


x = Deflate("abcabcababab")

x.LZ77_encoding()

print(x.current_list)
print(x.status)
x.huffman_probabilities()
print(x.nade_list)

x.create_huffman_tree()

print(x.huffman_tree)

x.huffman_tree.left.left.left.print_out()
