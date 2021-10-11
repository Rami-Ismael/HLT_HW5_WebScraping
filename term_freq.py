from io import FileIO
import os
import pickle
from typing import List
from main import pre_process 

def freq_dictionary(text_tokens: List[str]):
    freq_dict = dict()
    for token in text_tokens:
        if token in freq_dict.keys():
            freq_dict[token] = freq_dict[token] + 1
        else:
            freq_dict[token] = 1
    return freq_dict
def create_tf_dict( text_tokens: List[str]):
    freq_dict = dict()
    for token in text_tokens:
        if token in freq_dict.keys():
            freq_dict[token] = freq_dict[token] + 1
        else:
            freq_dict[token] = 1
    for t in freq_dict.keys():
        freq_dict[t] = freq_dict[t] / len( freq_dict.keys() )
    return freq_dict

def create_term_freq():
 vocab_set = set()
 freq_dict = dict()
 ## Create a list of freq_dict
 list_freq_dict = []
 ## the directory of all the output text
 path_1 =  os.path.join( os.getcwd(),  "output" )
 for files  in os.listdir( path_1 ):
     path_2 = os.path.join( path_1, files )
     for output_txt in os.listdir( path_2):
         ## add the set of 
         path_3 = os.path.join( path_2, output_txt )
         with open( path_3 , "r" ) as file:
             data = file.read()
             print( type ( data ) )
 
             tokens = pre_process(data)
 
 
             b =   freq_dictionary( tokens ) 
             list_freq_dict.append( create_tf_dict(tokens))
 
             for x in b.items():
                 if x[0] in freq_dict.keys():
                     freq_dict[x[0]] = freq_dict[x[0]]  +x[1]
                 else:
                     freq_dict[x[0]] = x[1]
             
             vocab_set.update(set ( tokens ))
 
 
 print(  sorted(freq_dict.items() , key = lambda x: x[1] , reverse = True ) , file  = open( "acc.txt" , "a"))
 
 ## the sorted list of tokens
 for x in sorted ( freq_dict.items() , key = lambda item: item[1] , reverse = True )[:40]  :
     print( x)
 
 file_to_write = open ( "term_freq.txt" , "wb")
 
 pickle.dump( freq_dict, file_to_write )


