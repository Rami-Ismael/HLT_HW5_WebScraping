from dataclasses import dataclass

@dataclass
class KB:
    """Class for keeping track of an item in inventory."""
    Entities: dict()
    def add_entity(self , name : str , freq: int , qid :int , relationship : dict) -> None:
        self.Entities[qid] = Entity(name, freq, qid , relationship)

@dataclass
class Entity:
    name:str
    freq:int
    qid:int
    realtion:dict()