import pickle
from kb import KB , Profession
from term_freq import create_term_freq
from UtilityFuncts import qid


## create_term_freq()


file_to_read = open("term_freq.pickle", "rb")


loaded_dictionary = pickle.load(file_to_read)

## Choose the 10 term 
throne = "throne"
tyrion = "tyrion"
stark = "stark"
robert = "robert"
arya = "arya"
cersei = "cersei"
dragon  = "dragon"
emilia  = "emilia"
melisandre = "melisandre"
jon = "jon"
top_term = [throne, tyrion, stark, robert , arya , cersei , dragon , emilia , melisandre , jon ]

## add throne 
kb = KB(Entities= dict())

## add throne and
freq = loaded_dictionary["throne"]
val = qid("throne")
relationship = {qid("emilia"):" She wants the throne"}
kb.add_entity( name = "throne" , freq = freq , qid = val , relationship = relationship )



## add tyrion
freq = loaded_dictionary["tyrion"]
val = qid("tyrion")
relationship = {qid("cersia"):" younger brother of Cerseia"}
kb.add_entity( name = "tyrion" , freq = freq , qid = val , relationship = relationship )

## stark
freq = loaded_dictionary["stark"]
val = qid("stark")
kb.add_entity( name = "stark" , freq = freq , qid = val , relationship = None )
kb.add_profession(val , Profession.Knight)

## robert
freq = loaded_dictionary["stark"]
val = qid("stark")
relationship = {qid("Lord Steffon Baratheron"):" oldest son and heir of Lord Steffon Baratheon"}
kb.add_entity( name = "stark" , freq = freq , qid = val , relationship = relationship )
kb.add_profession(val , Profession.Lord)

## arya 
freq = loaded_dictionary["arya"]
val = qid("arya")
kb.add_entity( name = "stark" , freq = freq , qid = val , relationship = None )

## cersei
freq = loaded_dictionary["cersei"]
val = qid("cersei")
kb.add_entity( name = "cersei" , freq = freq , qid = val , relationship = None )

for x in range( 5, len(top_term)):
    freq = loaded_dictionary[top_term[x]]
    val = qid(top_term[x])
    kb.add_entity( name = top_term[x] , freq = freq , qid = val , relationship = None )


kb.save_entities()

file_to_read = open("Entities.pickle", "rb")


loaded_dictionary = pickle.load(file_to_read)

print(loaded_dictionary)

