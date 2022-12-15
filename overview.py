import networkx as nx
import datetime
import pprint
import matplotlib.pyplot as plt
import numpy as np

def overview(G, create_overview_images=False):
    print(nx.info(G))
    print('node info')
    fraud_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 1]
    print('Number of fraud nodes: ', len(fraud_nodes))
    normal_nodes = [nd for nd in nx.nodes(G) if G.nodes[nd]['isp'] == 0]
    nodes = fraud_nodes + normal_nodes
    print('Number of fraud edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 1 and G.nodes[ed[1]]['isp'] == 1]))
    print('Number of normal edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 0 and G.nodes[ed[1]]['isp'] == 0]))
    print('number of edges: ', len(G.edges()))
    print('number of nodes: ', len(G.nodes()))


            
        

    if create_overview_images:
        print('number of edges with tx_hashes')
        num_instances_tx_hash = 0
        num_instances_tx_hash_and_usd_val_is_none = 0
        num_instances_tx_hash_is_none = 0
        total_transactions = 0


        labels_list = ['dex_accounts', 'gaming_accounts', 'wallet_app_accounts', 'cold_wallet_accounts', 'spam_token_deployer_accounts', 'token_contracts', 'tokenized_assets_contracts', 'dex_token_contracts', 'spam_token_contracts', 'gaming_token_contracts', 'wallet_app_token_contracts', 'account']
        # make a table of the number of nodes by label and save to file
        labels = []
        num_nodes = []
        for i,label in enumerate(labels_list):
            labels.append(label)
            num_nodes.append(len([nd for nd in G.nodes() if G.nodes[nd]['one_hot'][i] == 1]))

        # fig, ax = plt.subplots()
        # im = ax.imshow(num_nodes)
        # ax.set_xticks(np.arange(len(labels)))
        # ax.set_yticks(np.arange(len(labels)))
        # ax.set_xticklabels(labels)
        # ax.set_yticklabels(labels)
        # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
        #             rotation_mode="anchor")
        # for i in range(len(labels)):
        #     for j in range(len(labels)):
        #         text = ax.text(j, i, num_nodes[i],
        #                     ha="center", va="center", color="w")
        # ax.set_title("Number of nodes by label")
        # fig.tight_layout()
        # plt.savefig('num_nodes_by_label.png')

        #print labels and their number of nodes
        print('labels and their number of nodes')
        for i,label in enumerate(labels):
            print(label, num_nodes[i])

    
        # heatmap of the number of edges between labels with numbers in each cell and save to file
        labels = []
        num_edges = []
        for i,label in enumerate(labels_list):
            labels.append(label)
            num_edges.append([])
            for j,label in enumerate(labels_list):
                num_edges[i].append(len([ed for ed in G.edges() if G.nodes[ed[0]]['one_hot'][i] == 1 and G.nodes[ed[1]]['one_hot'][j] == 1]))

        fig, ax = plt.subplots()
        im = ax.imshow(num_edges)
        ax.set_xticks(np.arange(len(labels)))
        ax.set_yticks(np.arange(len(labels)))
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                    rotation_mode="anchor") 
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax.text(j, i, num_edges[i][j],
                            ha="center", va="center", color="w")
        ax.set_title("Number of edges between labels")
        fig.tight_layout()

        # print labels and their number of edges
        print('labels and their number of edges')
        for i,label in enumerate(labels):
            print(label, num_edges[i])

        
        

        # table for number of fraud accounts by label
        labels = []
        num_fraud_accounts = []
        for i, label in enumerate(labels_list):
            labels.append(label)
            num_fraud_accounts.append(len([nd for nd in G.nodes() if G.nodes[nd]['one_hot'][i] == 1 and G.nodes[nd]['isp'] == 1]))
        # make a table of the number of fraud accounts by label and save to file
        # fig, ax = plt.subplots()
        # im = ax.imshow(num_fraud_accounts)
        # ax.set_xticks(np.arange(len(labels)))
        # ax.set_yticks(np.arange(len(labels)))
        # ax.set_xticklabels(labels)
        # ax.set_yticklabels(labels)
        # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
        #             rotation_mode="anchor")
        # for i in range(len(labels)):
        #     for j in range(len(labels)):
        #         text = ax.text(j, i, num_fraud_accounts[i],
        #                     ha="center", va="center", color="w")
        # ax.set_title("Number of fraud accounts by label")
        # fig.tight_layout()
        # plt.savefig('num_fraud_accounts_by_label.png')

        # print labels and their number of fraud accounts
        print('labels and their number of fraud accounts:')
        for i,label in enumerate(labels):
            print(label, num_fraud_accounts[i])

        
        for edge in G.edges():
            for i in range(len(G[edge[0]][edge[1]])):
                total_transactions += 1
                if G[edge[0]][edge[1]][i]['tx_hash'] == 'not found':
                    num_instances_tx_hash += 1
                    if G[edge[0]][edge[1]][i]['usd_value'] == 0:
                        num_instances_tx_hash_and_usd_val_is_none += 1
                else:
                    num_instances_tx_hash_is_none += 1
        print('num_instances_tx_hash: ', num_instances_tx_hash)
        print('num_instances_tx_hash_and_usd_val_is_none: ', num_instances_tx_hash_and_usd_val_is_none)
        print('num_instances_tx_hash_is_none: ', num_instances_tx_hash_is_none)
        print('total_transactions: ', total_transactions)





    

    print('node features')
    for nd in G.nodes():
        print(nd, G.nodes[nd])
        for edge in G.edges(nd):
            print(edge)
        break

    # edge features
    print('edge features')
    for ed in G.edges():
        print(ed)
        for i in range(len(G[ed[0]][ed[1]])):
            print(G[ed[0]][ed[1]][i])
        break
        
