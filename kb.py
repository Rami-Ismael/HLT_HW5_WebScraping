from dataclasses import dataclass
from enum import Enum
import pickle
class Profession(Enum):
    Knight = "Knight"
    Lord = "Lord"
    Priestress = "Priestress"
@dataclass
class Entity:
    name:str
    freq:int
    qid:int
    father: str = None
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
    def determine_profession(self, qid):
        if self.Entities[qid].profession ==None:
            return "They have no Profession"
        return self.Entities[qid].profession.name
    ## assume that person have onl 1 to 1 relationship
    def add_realtionship(self, qid , rela) -> None:
        try:
            self.Entities[qid].relationship = self.Entities[qid].relationship.union( rela )
        except:
            self.Entities[qid].relationship =  rela
    def number_of_profession(self) -> int:
        return len(Profession)
    def freq(self, qid) -> int:
        return self.Entities[qid].freq
    

