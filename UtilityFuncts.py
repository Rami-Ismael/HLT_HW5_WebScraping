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