import math
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

#Takes in a long line of text and returns a list of Nade objects with their probabilities
def get_huffman_probabilties(text):
    """
    Takes a string and returns a list of Nade objects with their probabilities.
    """
    # Create a dictionary to count the frequency of each character
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # Create a list of Nade objects with their probabilities
    nades = []
    for char, freq in frequency.items():
        nades.append(Nade(name=char, value=freq))

    return nades

#this takes in a list of Nade objects and builds a binary huffman tree
def huffman_tree(nades):
    #print("initial nades:")
    nades.sort(key=lambda x: x.value)
    #for i in nades: i.pertinent_info()  # Print initial nades for debugging
    while len(nades) > 1:
        left = nades.pop(0)
        right = nades.pop(0)
        new_node = Nade(name=left.name + right.name,  value=left.value + right.value)
        new_node.left = left
        new_node.right = right
        left.parent = new_node
        right.parent = new_node
        nades.append(new_node)
        nades.sort(key=lambda x: x.value)

    return nades[0]  # Return the root of the tree

#this function takes in a huffman tree(which is the starter nade) and returns a dictionary of huffman codes
def derive_huffman_codes(huffman_tree):
    huff_codes = dict()
    queue = []
    visited = set()
    queue.append((huffman_tree,""))  # Start with the root of the tree
    while len(queue) > 0:
        current_node, current_code = queue.pop(0)
        #print("current_node:", current_node.name, "current_code:", current_code, "type:", type(current_node))
        visited.add(current_node.name)
        if current_node.left is None and current_node.right is None:  # If it's a leaf node
            
            huff_codes[current_node.name] = current_code  # Store the code for the leaf node
        else:
            queue.append((current_node.left,current_code + "0")) #we go left
            queue.append((current_node.right,current_code + "1")) #we go right
    return huff_codes  # Return the dictionary of huffman codes


# This function takes in the string representation of a binary number (no 0b prefix) and converts it into a list of bytes.
def byte_manager(binary_number):
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


    
    



# This function encodes a text using the huffman codes and returns a list of bytes representing the encoded text.
def encode_text_huffman(text,huffman_codes={}):
    binary_string = ""
    for i in text:
        binary_string += huffman_codes[i]
    return byte_manager(binary_string)  # Convert the binary string to a byte list




#converts a UTF-8 letter in string format into a binary representation
def UTF_letter_to_binary(string):
    if len(string) != 1: return None
    new_byte_list = string.encode('utf-8')  # Encode the string to bytes
    return new_byte_list


#Formats a large number as a list of integer bytes
def format_large_number_as_bytes(number):
    byte_list = []
    binary_representation = bin(number)[2:]  # Convert the number to binary and remove the '0b' prefix
    if len(binary_representation) % 8 != 0:
        binary_representation = '0' * (8 - len(binary_representation) % 8) + binary_representation  # Pad the binary representation to make it a multiple of 8 bits
    slice = binary_representation[-8:]  # Get the last 8 bits

    for i in range(0,int(len(binary_representation)/8)):
        slice = binary_representation[i * 8: (i + 1) * 8]  # Get the next 8 bits
        byte_list.append(int(slice,2)) # Append the byte to the list
    return byte_list


#generates a header for the huffman encoded text, which itself is a list of bytes in integer form
def generate_header(text,huffman_codes):
    byte_list = []
    length_of_unencoded_text = len(text.encode('utf-8'))  # Get the length of the encoded text 

    file_size_byte_list =format_large_number_as_bytes(length_of_unencoded_text)

    for i in range(8 - len(file_size_byte_list)):
        byte_list.append(0) # Pad the byte list with zeros to make it 8 bytes long

    byte_list.extend(file_size_byte_list)  # Add the length of the unencoded text to the header

    number_of_unique_characters = len(huffman_codes)  # Get the number of unique characters in the text

    unique_character_byte_list = format_large_number_as_bytes(number_of_unique_characters)

    for i in range(2 - len(unique_character_byte_list)):
        byte_list.append(0) # Pad the byte list with zeros to make it 2 bytes long

    byte_list.extend(unique_character_byte_list) # Add the number of unique characters to the header

    byte_list.extend(generate_variable_codes(huffman_codes)) #add the variable huffman codes

    return byte_list

# Generates variable codes for the header based on the huffman codes
def generate_variable_codes(huffman_codes):
    byte_list = []
    for k,v in huffman_codes.items():
        
        #we need to convert the character to its UTF-8 byte representation but also add some compatability for the length of the UTF-8 character(what if its more than 1 byte?)
        byte_list.extend(UTF_letter_to_binary(k))  # Convert the character to its UTF-8 byte representation
        whole_byte_length = len(v)
        byte_list.append(whole_byte_length)  # Append the length of the huffman code which is one byte
        
        byte_code = byte_manager(v) #add the actual code
        byte_list.extend(byte_code)
        count = 0
        
    #x = pad_bytes_to_multiple_of_eight(byte_list)
    return byte_list



## This function takes an input string, generates the Huffman probabilities, builds the Huffman tree,
## derives the Huffman codes, and then encodes the input string into a list of bytes.
def encrypt_string_to_bytes(input_string):
    probability_list = get_huffman_probabilties(input_string)

    huffman_tree_root = huffman_tree(probability_list)

    huffcode = derive_huffman_codes(huffman_tree_root)

    byte_list = []

    byte_list.extend(generate_header(input_string,huffcode))  # Generate the header and add it to the byte list
    byte_list.extend(encode_text_huffman(input_string, huffcode))  # Encode the text and add it to the byte list

    return bytes(byte_list) # Return the complete byte list containing the header and encoded text


#Compress a targeted .txt file
def compress_file(filepath):
    file_object = None
    content = None
    compress_object = None
    try:
        file_object = open(filepath, 'r') # Open the file in read mode, make it read it in utf-8 format
        content = repr(file_object.read())  # Read the content of the file

        content = content.strip("'")
        encrypted_content = encrypt_string_to_bytes(content)  # Encrypt the content using Huffman encoding, it is a list of bytes
        print("test")
        compress_object = open(filepath.split(".")[0] + ".bin", 'wb')  # Open a new file for writing the compressed content

        compress_object.write(encrypted_content)  # Write the encrypted content to the new file
    except:
        print("File does not exist.")
    finally:
        if file_object:
            file_object.close() # Close the file 
            compress_object.close()
            print(filepath,"has been successfully compressed!")




#Decompresses a targeted bin file and returns a list of strings.
def decompress_file(filepath):
    file_object = None
    content = None
    decoded_message = ""
    try:
        file_object = open(filepath, 'rb')  # Open the file in binary read mode
        content = list(file_object.read())  # Read the content of the file
        content = pad_bytes_to_multiple_of_eight(content)

        # Here you would need to implement the logic to decode the content using Huffman decoding
        # For now, we will just print the content as bytes
        #print("Decompressed content:", list(content))
        thruple = decode_header(content)
        huffman_tree = thruple[0]
        original_size = thruple[1]
        encoded_message = thruple[2]
        
        
        encoded_message = ''.join(encoded_message)
        
        
        

        counter = 0
        current_node = huffman_tree


        
        while counter < len(encoded_message):
            
            if current_node.left == None and current_node.right == None:

                decoded_message += current_node.name
                current_node = huffman_tree # we reset back to the root node to decode another letter
                
                if len(decoded_message.encode('utf-8')) >= original_size:break #if the decoded_message reaches size of the original size we are finished and stop the loop.

            else:

                if encoded_message[counter] == "0": current_node = current_node.left
                elif encoded_message[counter] == "1": current_node = current_node.right
                counter += 1 # we move onto the next bit in the sequence
    except:
        print("File does not exist.")
        file_object.close()
                
            
    finally:
        if file_object:
            file_object.close()  # Close the file (this is crucial!)
            
            return decoded_message.strip('"').split("\\n")
#decompress_file("larrytext.bin")  # Call the decompress_file function with the file path


# takes a list of string bytes and formats it as a large number
def format_bytes_as_large_number(byte_list):
    binary_representation = ""
    for i in byte_list:
        binary_representation += i
    return int(binary_representation, 2)  # Convert the binary representation to an integer


# This function pads a list of bytes to make its length a multiple of 8. converts the ints to string bytes
def pad_bytes_to_multiple_of_eight(byte_list):
    for byte in range(len(byte_list)):
        length_of_byte = len(bin(byte_list[byte])[2:])
        byte_list[byte] = bin(byte_list[byte])[2:] # Convert the byte to string binary and remove the '0b' prefix
        if 8 - length_of_byte != 0:
            byte_list[byte] = "0" * (8 - length_of_byte) + byte_list[byte] # Pad the byte with zeros to make it 8 bits long
    return byte_list  # Return the padded byte list

# This function decodes a header from a list of bytes and returns the relevant information. takes in string bytes
def decode_header(header):
    huffcode = dict()
    file_size_info = format_bytes_as_large_number(header[:8])  # Get the first 8 bytes for the file size
    unique_characters_info = format_bytes_as_large_number(header[8:10]) #get the next 2 bytes for the number of unique characters
    variable_codes_info = header[10:]  # Get the rest of the bytes for the variable codes
    #remainder = header[10 + 3 * unique_characters_info:] #This is the raw encoded text. This function is not responsible for doing anything to it..yet
    
    for i in range(unique_characters_info):
        character_byte_length = determine_UTF_byte_length(variable_codes_info[0])
        singular_byte = variable_codes_info[0]

        isolated_byte_list = variable_codes_info[:character_byte_length]

        variable_codes_info = variable_codes_info[character_byte_length:]#remove the utf-8 encoding bytes from the list

        for i in range(len(isolated_byte_list)): isolated_byte_list[i] = int(isolated_byte_list[i],2)

        UTF_letter = bytes(isolated_byte_list).decode('utf-8') #problem line
        


        code_length = format_bytes_as_large_number([variable_codes_info[0]]) #length of the code in bits

        variable_codes_info = variable_codes_info[1:]#remove the singular byte representing the actual code length in bits




        code_length_in_bytes = int(code_length/9) + 1
        string_code = ""
        actual_variable_code = variable_codes_info[:code_length_in_bytes]
        pieced_together_raw_variable_code = ""

        for j in actual_variable_code: pieced_together_raw_variable_code += j

        for j in range(code_length): string_code += pieced_together_raw_variable_code[j]
        huffcode[UTF_letter] = string_code

        variable_codes_info = variable_codes_info[code_length_in_bytes:]#remove that particular utf-8 encoding, length of bits, and the actual variable code for the next code to be processed.
    print("erm")
    
    return regenerate_huffman_tree_from_codes(huffcode),file_size_info,variable_codes_info#variable_codes_info now just has the encoded binary

#determine the length of the UTF-8 binary encoding from just the first byte
def determine_UTF_byte_length(singular_string_byte):
    difference = len(singular_string_byte) - len(singular_string_byte.lstrip("1"))
    if difference == 0: return 1
    return difference


#generate an entire huffman tree from the provided huffman codes. Returns the root node.
def regenerate_huffman_tree_from_codes(huffcodes):
    nade_count = 1
    root_node = Nade(str(nade_count))
    nade_count += 1
    for letter,code in huffcodes.items():
        current_node = root_node
        for i in range(len(code)):
            if code[i] == "0":
                if current_node.left == None:
                    if i == (len(code) - 1): # if this is the last letter in the code
                        current_node.left = Nade(letter)
                        current_node.left.parent = current_node
                    else:
                        current_node.left = Nade(str(nade_count))
                        current_node.left.parent = current_node
                        nade_count += 1
                        current_node = current_node.left
                else:
                    current_node = current_node.left
            else: # if code is 1
                if current_node.right == None:
                    if i == (len(code) - 1): # if this is the last letter in the code
                        current_node.right = Nade(letter)
                        current_node.right.parent = current_node
                    else:
                        current_node.right = Nade(str(nade_count))
                        current_node.right.parent = current_node
                        nade_count += 1
                        current_node = current_node.right
                else:
                    current_node = current_node.right
    return root_node





while True:
    query = input("Compress(c) or Decompress(d) file: ").lower()
    if query == "c":
        file_name = input("Enter the name of the .txt file you would like to compress: ") + ".txt"
        compress_file(file_name)
    elif query == "d":
        file_name = input("Enter the name of the .bin file you would like to decompress: ") + ".bin"
        stored_contents = decompress_file(file_name)

        print("Contents of",file_name,":")
        for i in stored_contents:print(i)
    elif query == "exit":break


