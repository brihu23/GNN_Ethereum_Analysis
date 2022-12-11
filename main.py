import pickle 
import networkx as nx
import random
from extract_random_nodes import extract_random_nodes
from overview import overview

'''
To get setup:

Download the pkl file from https://www.kaggle.com/datasets/xblock/ethereum-phishing-transaction-network?resource=download
(It is too large to upload to GitHub so to run the code locally, you will need to download it from Kaggle)

'''

# loading full dataset
def load_pickle(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)
print('Loading pickle file...')
G = load_pickle('./MulDiGraph.pkl')
print('Pickle file loaded.')
print('Overview of the graph (first 10 nodes and edges')
overview(G)

# extracting random sample of nodes as done in paper

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

'''Replicating their experiment'''
# TODO: Add Ethereum labels to the subgraph (see etherscan_labels.py) (Brihu)
# TODO Amplify random nodes with neighbors nodes after labelling (Brihu)
# TODO: Run Heterogeneous Graph Neural Network on the subgraph as shown in paper (Ez + Boris)

'''Additional work that we are doing'''
# TODO: Get transaction hash for each edge --> save in CSV file (Brihu)
# TODO: Get transaction value and other metadata for each edge in each edge --> save in CSV file and add to subgraph at runtime (Brihu)
# TODO: Add any any extra labels that we want (see etherscan_labels.py) (Brihu)
# TODO: Run Heterogeneous Graph Neural Network on the subgraph as shown in paper (Ez + Boris)

'''Writeup'''

print('Done.')