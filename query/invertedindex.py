
import os
from reducewordstobase import reducewords
import reducewordstobase
import pickle
import networkx as nx
# assign directory

web_graph = nx.read_gpickle("web_graph.gpickle")


textfiles={}
dictionary={}
wordlist=[]
for node_index in range(web_graph.number_of_nodes()):
    text = web_graph.nodes[node_index]['page_content']
    # checking if it is a file
    
    processedtext=reducewords(text)
    textfiles[node_index]=processedtext
    for word in processedtext:
        wordlist.append(word)
        if word not in dictionary.keys():
            dictionary[word]=[]
        if node_index not in dictionary[word]:
            dictionary[word].append(node_index)
'''we iterate through every file and for every unique word we create 
list after processing it and reducing it to base form .
We store it in a dict where key is word and value is a list containing 
all the filenames containing that word'''

wordlist=set(wordlist)

filename = 'dictionary'
outfile = open(filename,'wb')
pickle.dump(dictionary,outfile)
outfile.close()
'''dictionary is pickled'''

filename = 'wordlist'
outfile = open(filename,'wb')
pickle.dump(wordlist,outfile)
outfile.close()
'''all the processed words are stored in wordlist'''

print(dictionary)

