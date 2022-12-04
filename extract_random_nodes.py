# Pick up 2,230 nodes from the network, consisting of 1,165 fraud nodes and 1,165 normal nodes chosen randomly.
import networkx as nx
import random
def extract_random_nodes(G, n_fraud, n_normal):
    # Pick up fraud nodes
    fraud_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 1]
    # Pick up normal nodes
    normal_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 0]
    # Pick up n_fraud nodes from fraud_nodes
    fraud_nodes = random.sample(fraud_nodes, n_fraud)
    # Pick up n_normal nodes from normal_nodes
    normal_nodes = random.sample(normal_nodes, n_normal)
    # Combine fraud_nodes and normal_nodes
    nodes = fraud_nodes + normal_nodes
    # get neighbors of nodes
    neighbors = []
    for nd in nodes:
        neighbors += list(G.neighbors(nd))
    # Combine nodes and neighbors
    nodes += neighbors
    # Remove duplicates
    nodes = list(set(nodes))
    # Return the subgraph
    return G.subgraph(nodes)