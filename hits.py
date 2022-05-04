#%%
from locale import normalize
import networkx as nx #pip install networkx
import numpy as np
from pyparsing import NoMatch
from numpy.linalg import eig
import matplotlib
from query.query import querylol

#: this is our entire web graph
web_graph = nx.read_gpickle("web_graph.gpickle")

def baseset(web_graph, result):
    """generates base set from webgraph and query result

    Args:
        web_graph : web graph of networkx type
        result : a list of nodes satisfying query

    Returns:
        resultbase: returns base set
    """
    #: adjacency matrix of the entire web graph
    adj=(nx.to_numpy_array(web_graph))

    #: root set represented by a 1-0 matrix denoting presence/absence of a node
    root=np.zeros((1,web_graph.number_of_nodes()))
    for i in result:
        root[0,i]=1

    #: set represented by a 1-0 matrix denoting nodes that are connected to from root set 
    base1=np.dot(root,adj)

    #: set represented by a 1-0 matrix denoting nodes that connect to the root set 
    base2=np.dot(root,np.transpose(adj))

    #: set represented by a 1-0 matrix denoting nodes that are present in base set
    base=base1+base2+root

    #: the base set
    resultbase=[]


    for i in range(web_graph.number_of_nodes()):
        if base[0,i]>0:
            resultbase.append(i)
            
    return resultbase
        

def hitsscores(web_graph, resultbase):
    """hitscores calculates the hub scores and authority scores

    Args:
        web_graph : web graph of networkx type
        resultbase : a list of nodes satisfying query

    Returns:
        hubscore : list of hubscores
        authorityscores: list of authority scores
    """
    #: subgraph derived from `web_graph` containing only the base set nodes and their edges
    subgraph=web_graph.subgraph(resultbase)

    #: adjacency matrix of base set `resultbase` corresponding to `subgraph`
    subadj=(nx.to_numpy_array(subgraph, nodelist=resultbase))

    #: `subadj` * `subadj` transpose
    aat=np.dot(subadj, np.transpose(subadj))

    #: `subadj` transpose * `subadj`
    ata=np.dot(np.transpose(subadj), subadj)

    #: hubscore `h` calculated using eigen method
    wh,h=eig(aat)
    #: hubscore `a` calculated using eigen method
    wa,a=eig(ata)

    #: sort the eigenvalues in descending order
    sorted_index = np.argsort(wh)[::-1]
    sorted_eigenvalue = wh[sorted_index]
    #: similarly sort the eigenvectors 
    sorted_eigenvectors = h[:,sorted_index]
    #: hub score set as the principal eigen vector  
    hubscore = np.real(sorted_eigenvectors[:,0:1]/sorted_eigenvectors[:,0:1].sum())[:,0]
    #: sort the eigenvalues in descending order
    sorted_index = np.argsort(wa)[::-1]
    sorted_eigenvalue = wa[sorted_index]
    #: similarly sort the eigenvectors 
    sorted_eigenvectors = a[:,sorted_index] 
    #: authority score set as the principal eigen vector  
    authorityscore = np.real(sorted_eigenvectors[:,0:1]/sorted_eigenvectors[:,0:1].sum())[:,0]
    
    print("hubscore")
    for i in range(subgraph.number_of_nodes()):
        print(str(resultbase[i])+": "+str(round(hubscore[i],3)))
    print("authorityscore")
    for i in range(subgraph.number_of_nodes()):
        print(str(resultbase[i])+": "+str(round(authorityscore[i],3)))
        
    
    #: draw graph
    #pos = {i: web_graph.nodes[i]['pos'] for i in range(len(web_graph.nodes))}
    #nx.draw(subgraph, pos, with_labels=True, node_size=300)
    
    return hubscore, authorityscore

if __name__ == "__main__":
#: query is done and resulting list of pages matching the query is returned
    result=querylol()
    resultbase=baseset(web_graph, result)
    hubscore, authorityscore=hitsscores(web_graph, resultbase)

    sorted_index = np.argsort(hubscore)[::-1]
    #: sort pages according to hub score
    sorted_hubscore={}
    for i in range(len(resultbase)):
        sorted_hubscore[i+1]=resultbase[sorted_index[i]]


    sorted_index = np.argsort(authorityscore)[::-1]
    #: sort pages according to authority score
    sorted_authscore={}
    for i in range(len(resultbase)):
        sorted_authscore[i+1]=resultbase[sorted_index[i]]


    print("hub rank")
    print(sorted_hubscore)
    print("authority rank")
    print(sorted_authscore)

# %%