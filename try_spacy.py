import spacy
from spacy.kb import KnowledgeBase

def qid( word , primes ):
    prim_freq = dict()
    for x in word:
        if  primes[ ord(x-97)] in prim_freq.keys(): 
            prim_freq[ primes[ ord(x-97)] ]  = prim_freq[ primes[ ord(x-97)]] +1
        else:
            prim_freq[ primes[ ord(x-97)]]= 1
    val = 0
    for x  in prim_freq.items():
        prime_val = x[0]
        freq = x[1]
        val  = prime_val *freq
    return val
            



if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    text = "Tennis Champion ermsaon was expeceted to win championships"

    doc = nlp(text)

    print ( type ( doc ) )
    print (  doc.vector ) 


    ## Choose the 10 term 
    throne = "throne"
    tyrion = "tyrion"
    stark = "stark"
    martin = "martin"
    arya = "arya"
    cersei = "cersei"
    dragon  = "dragon"
    emilia  = "emilia"
    melisandre = "melisandre"
    kingdom = "kingdom"
    top_term = [throne, tyrion, stark, martin , arya , cersei , dragon , emilia , melisandre , kingdom ]
    ## Create qid
    n = 30
    primes = []
    for i in range( 2 , n+1 ):
        for j in range(2, int(i ** 0.5) + 1):
            if i%j ==0:
                break
        else:
            primes.append(i)

    ## Create the knowledgebase using spacy
    kb = KnowledgeBase( vocab = nlp.vocab , entity_vecotr_lenght = 300)

    ## add all the term into the knowldege base
    for x in top_term:
        desc_doc = nlp(x)
        desc_enc = desc_doc.vector
        kb.add_entity( entity = qid( x , primes ) , entity_vectors = desc_enc , freq = )
