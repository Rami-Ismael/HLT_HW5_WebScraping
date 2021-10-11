import os
import pickle


def openFile(filepath: str, mode: str, encoding: str = None):
    """Function to open a file path that works cross platform"""
    return open(os.path.join(os.getcwd(), filepath), mode, encoding=encoding)


def openPickle(filepath: str, objName: str = ""):
    """Function to open up and return a pickled object from a pickle file..."""
    with openFile(filepath, mode="rb") as pickleFile:
        obj = pickle.load(pickleFile)
        print(f"Successfully read in the obj: {objName} from \'{filepath}\'")
        return obj


def writePickle(filepath: str, object, objName: str = ""):
    """Function to open up and write an object to a pickle file..."""
    with openFile(filepath, mode="wb") as pickleFile:
        pickle.dump(object, pickleFile)
        print(f"Successfully wrote out the obj: {objName} to \'{filepath}\'")
def qid( word ):
    ## Create qid
    n = 10000
    primes = []
    for i in range( 2 , n+1 ):
        for j in range(2, int(i ** 0.5) + 1):
            if i%j ==0:
                break
        else:
            primes.append(i)
    prim_freq = dict()
    for x in word:
        if  primes[ ord(x) - 97 ] in prim_freq.keys(): 
            prim_freq[ primes[ ord(x) -97 ] ]  = prim_freq[ primes[ ord(x) -97 ]] +1
        else:
            prim_freq[ primes[ ord(x) -97 ]]= 1
    val = 0
    for x  in prim_freq.items():
        prime_val = x[0]
        freq = x[1]
        val   =  (   prime_val *freq)  + val
    return val
            