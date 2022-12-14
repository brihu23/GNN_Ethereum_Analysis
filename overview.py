import networkx as nx
import datetime
import pprint

def overview(G):
    print(nx.info(G))
    print('node info')
    # fraud_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 1]
    # print('Number of fraud nodes: ', len(fraud_nodes))
    # normal_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 0]
    # nodes = fraud_nodes + normal_nodes
    # print('Number of fraud edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 1 and G.nodes[ed[1]]['isp'] == 1]))
    # print('Number of normal edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 0 and G.nodes[ed[1]]['isp'] == 0]))
    # print('number of edges: ', len(G.edges()))
    # print('number of nodes: ', len(G.nodes()))

    # Traversal nodes:
    # for idx, nd in enumerate(nx.nodes(G)):
    #     print(G.nodes[nd])
    #     if (idx > 10):
    #         break
        
    print('edge info')
    # print number of edges that have a txhash
    # print('Number of edges with txhash: ', len([ed for ed in nx.edges(G) if G[ed[0]][ed[1]][0]['txhash'] != 'not found']))
    # # Travelsal edges:
    # for ind, edge in enumerate(nx.edges(G)):
    #     (u, v) = edge
    #     eg = G[u][v][0]
    #     print(edge)
    #     print(G[u][v])
    #     # print(G[u][v])
    #     timestamp = eg['timestamp']
    #     amo, tim = eg['amount'], eg['timestamp']
    #     if (ind > 10):
    #         break
