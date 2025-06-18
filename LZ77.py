class Deflate:
    def __init__(self,input_string):
        self.encoded_string = ""
        self.unencoded_string = input_string
        self.current_list = []
    
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

    def LZ77_encoding(self,input_string):
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

        






        


