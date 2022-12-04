import pickle 
import networkx as nx
import random
from extract_random_nodes import extract_random_nodes
from overview import overview

def load_pickle(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)
print('Loading pickle file...')
G = load_pickle('./MulDiGraph.pkl')
print('Pickle file loaded.')
print('Overview of the graph (first 10 nodes and edges')
overview(G)
print('Extracting random nodes...')
G_subgraph = extract_random_nodes(G, 1165, 1165)
print('Random nodes extracted.')
overview(G_subgraph)
# save the subgraph
print('Saving the subgraph...')
# save graph as pickle file
with open('./MulDiGraph_subgraph.pkl', 'wb') as f:
    pickle.dump(G_subgraph, f)
print('Subgraph saved.')


# TODO: Choose Ethereum labels and get associated wallets/accounts
# TODO: Add Ethereum labels to the subgraph (pick more than what they just did in the paper)
# TODO: Get transaction hash for each edge --> save in CSV file
# TODO: Get transaction value and other metadata for each edge in each edge --> save in CSV file and add to subgraph at runtime
# TODO: Run GNN pipeline on the subgraph as shown in paper

print('Done.')