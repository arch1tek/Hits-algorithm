import os
from reducewordstobase import reducewords
import reducewordstobase
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import pickle
import networkx as nx


tokenizer = RegexpTokenizer(r'\w+')

def tokenizetext(text):
    text_tokens = tokenizer.tokenize(text.lower())
    print("ded")
    return text_tokens
# assign directory
allunique=[]
web_graph = nx.read_gpickle("web_graph.gpickle")

for node_index in range(web_graph.number_of_nodes()):
    text = web_graph.nodes[node_index]['page_content']
    for word in tokenizetext(text):
        allunique.append(word)
allunique=set(allunique)
filename = 'allunique'
outfile = open(filename,'wb')
pickle.dump(allunique,outfile)
outfile.close()
'''calculates all the unique words in 
the dataset without processing and stores it in allunique list by pickling'''