#%%
import pickle
import os
from typing import final
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from query.editdistance import levenshtein
from query.wildcard import matchwildcard
import networkx as nx
'''importing libraries for querying'''

def querylol(): 
    ps=PorterStemmer()
    wnl=WordNetLemmatizer()
    '''initialized stemmer and lemmatizer'''

    web_graph = nx.read_gpickle("web_graph.gpickle")
    filelist=[node_index for node_index in range(web_graph.number_of_nodes())]
    '''created a filelist containing name of files in dataset'''

    def AND(lst1, lst2):
        return set(lst1) & set(lst2)
    def OR(lst1, lst2):
        return set(lst1) | set(lst2)
    def DIFF(lst1, lst2):
        return set(lst1)-set(lst2)
    def NOT(lst1):
        return set(filelist)-set(lst1)
    def XOR(lst1, lst2):
        return set(lst1)^set(lst2)
    '''defined functions to be used while querying'''

    filename='dictionary'
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()
    '''loaded the dictionary containing inverted index into new_dict
    from pickled file named dictionary'''

    filename='allunique'
    infile = open(filename,'rb')
    allunique = pickle.load(infile)
    infile.close()
    '''loaded the allunique list containing all unique words in all docs into allunique list
    from pickled file named allunique'''

    filename='wordlist'
    infile = open(filename,'rb')
    wordlist = pickle.load(infile)
    infile.close()

    result=[]
    connectors=['AND','NOT', 'OR','XOR','(', ')']
    '''initialized lists result to store final filelist and
    connectors to differentiate from other words'''

    print("enter query: ")
    query=input()
    query=query.split() 
    finalquery=""
    for word in query:
        if(word in connectors):
            if (word=='AND'):
                finalquery+='&'

            elif (word=='OR'): 
                finalquery+='|'

            elif (word=='XOR'): 
                finalquery+='^'

            elif(word=='NOT'):
                finalquery+='set(filelist)-'

            elif(word=='('):
                finalquery+='('
            
            elif(word==')'):
                finalquery+=')'
        #checked for connectors

        elif('*' in word):
            print("for "+word)
            finalquery+=str(matchwildcard(word))
        #checked for wildcard
        else:
            finalquery+='set('
            newword=ps.stem(wnl.lemmatize(word.lower()))
            if newword not in allunique:
                if newword not in wordlist:
                    print(word+": not in dictionary")
                    levenshtein(newword)
                    exit() 
            if newword not in new_dict.keys():
                print(newword+': is a stop word')
                exit(0)
            finalquery+='new_dict[\''
            finalquery+=str(newword)

            finalquery+='\'])'
    '''we take input and parse the query to a suitable mathematical form named finalquery'''
    print(finalquery)
    result=eval(finalquery)
    '''query is evaluated'''
    count=1
    result=list(result)
    print(result)
    print("results:")
    for filename in result:
        print(count)
        print(str(filename)+ "\n")
        count=count+1
    '''results are printed'''
    return result


# %%
