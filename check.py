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
rob  = "rob"
emilia  = "emilia"
melisandre = "melisandre"
jon = "jon"
top_term = [throne, tyrion, stark, robert , arya , cersei , rob , emilia , melisandre , jon ]

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
kb.add_entity( name = "arya" , freq = freq , qid = val , relationship = None )

## cersei
freq = loaded_dictionary["cersei"]
val = qid("cersei")
kb.add_entity( name = "cersei" , freq = freq , qid = val , relationship = None )

for x in range( 5, len(top_term)):
    freq = loaded_dictionary[top_term[x]]
    val = qid(top_term[x])
    kb.add_entity( name = top_term[x] , freq = freq , qid = val , relationship = None )

## add rob
kb.add_realtionship( qid("rob") , {qid("Lord Eddard Stark of Winterfell") : "The eldest sone of Eddard Stark of Winterfell"})

## emilia
kb.add_realtionship(qid("emilia"), {qid("Targaryen"):"She is a Targaryen"})

## melisandre
kb.add_realtionship(qid( "melisandre"), {qid("melisandre") : "She is hte Red Priestress"})
kb.add_profession(qid("melisandre") , Profession.Priestress) 

## jon
kb.add_realtionship( qid( "jon") , { qid("lyanna") : "He is the sone of Lyanna Stark " })


kb.save_entities()

file_to_read = open("Entities.pickle", "rb")


loaded_dictionary = pickle.load(file_to_read)

print(loaded_dictionary)

## What is stark profession
print("What is Start profession? ")
print( " Stark Profession is "+kb.determine_profession(qid("stark")) )

## How many profession are the in game throne
print("How many professionals are in the game of throne")
print( "There is "+ str(kb.number_of_profession()) + " profession in game of throne")

## how many time did jon appear in the movie
print( "How many time did jon appear in the game throne")
print( "Jon appear "+ str(kb.freq(qid("jon"))) +" times in game of throne")

