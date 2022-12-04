import networkx as nx

def overview(G):
    print(nx.info(G))
    print('node info')
    # Traversal nodes:
    for idx, nd in enumerate(nx.nodes(G)):
        print(nd)
        print(G.nodes[nd]['isp'])
        if (idx > 10):
            break
        
    print('edge info')
    # Travelsal edges:
    for ind, edge in enumerate(nx.edges(G)):
        (u, v) = edge
        eg = G[u][v][0]
        print(edge, eg, ind)
        amo, tim = eg['amount'], eg['timestamp']
        if (ind > 10):
            break
