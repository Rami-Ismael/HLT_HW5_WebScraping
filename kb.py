from dataclasses import dataclass
from enum import Enum
import pickle
class Profession(Enum):
    Knight = 0
    Lord = 1
    Priestress = 2
@dataclass
class Entity:
    name:str
    freq:int
    qid:int
    father: name = None
    relationship:dict()  = None
    profession: Profession = None
@dataclass(init = True)
class KB:
    """Class for keeping track of an item in inventory."""
    Entities: dict()  
    def add_entity(self , name : str , freq: int , qid :int , relationship : dict) -> None:
        self.Entities[qid] = Entity(name, freq, qid , relationship)
    def save_entities(self) -> None:
        file_to_write = open ( "Entities.pickle" , "wb")
        pickle.dump( self.Entities, file_to_write )
    def add_profession(self, qid , profession) -> None:
        self.Entities[qid].profession = profession
    ## assume that person have onl 1 to 1 relationship
    def add_realtionship(self, qid , rela) -> None:
        self.Entities[qid].relationship = self.Entities[qid].relationship.union( rela )

