import dill as pickle
import networkx as nx
import random
from extract_random_nodes import extract_random_nodes_and_label
from overview import overview
import datetime
from get_tx_hash import get_tx_hash
from get_tx_hash_v2 import get_tx_hash_v2
from extract_random_nodes import to_iso_time
from get_tx_value_v2 import get_tx_value_v2

'''
To get setup:

Download the pkl file from https://www.kaggle.com/datasets/xblock/ethereum-phishing-transaction-network?resource=download
(It is too large to upload to GitHub so to run the code locally, you will need to download it from Kaggle)
https://arxiv.org/pdf/2203.12363.pdf

'''


def main():


    is_subgraph = True
    nodes = 1000
    maingraph_path = './MulDiGraph.pkl'
    subgraph_save_path = './MulDiGraph_subgraph_2000final_backup.pkl'
    subgraph_path = './MulDiGraph_subgraph_2000final_backup.pkl'
    # preload_path = None
    preload_path = './unique_senders_receivers.json'
    skipLoading = True
    create_overview_images = False

    def load_pickle(fname):
        with open(fname, 'rb') as f:
            return pickle.load(f)

    
    # loading full dataset
    if not is_subgraph:
        print('Loading graph...')
        startTime = datetime.datetime.now()
        G = load_pickle(maingraph_path)
        print('Pickle file loaded.')
        # overview(G)
        endTime = datetime.datetime.now()
        print('Time taken to load the graph: ', endTime - startTime)

    if is_subgraph:
        print('Loading subgraph...')
        startTime = datetime.datetime.now()
        G = load_pickle(subgraph_path)
        print('Prev Subgragh Pickle file loaded.')
        overview(G, create_overview_images)
        endTime = datetime.datetime.now()
        print('Time taken to load the subgraph: ', endTime - startTime)
        



    # extracting random sample of nodes as done in paper
    startTime = datetime.datetime.now()
    print('Extracting and labeling random nodes...')
    G_subgraph = extract_random_nodes_and_label(G, nodes, nodes, is_subgraph, preload_path, skipLoading)
    print('Random nodes extracted and labelled.')
    overview(G_subgraph)
    endTime = datetime.datetime.now()
    print('Time taken to extract random nodes and label: ', endTime - startTime)
    # save the subgraph

    startTime = datetime.datetime.now()
    print('Saving the subgraph...')
    # save graph as pickle file
    with open(subgraph_save_path, 'wb') as f:
        pickle.dump(G_subgraph, f)
    print('Subgraph saved.')
    print('Time taken to save the subgraph: ', endTime - startTime)

    endTime = datetime.datetime.now()


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
    

if __name__ == '__main__':
    main()