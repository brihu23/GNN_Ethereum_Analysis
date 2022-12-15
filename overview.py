import networkx as nx
import datetime
import pprint
import matplotlib.pyplot as plt

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

        for edge in G.edges():
            for i in range(len(G[edge[0]][edge[1]])):
                total_transactions += 1
                if G[edge[0]][edge[1]][i]['tx_hash'] == 'not found':
                    num_instances_tx_hash += 1
                    if G[edge[0]][edge[1]][i]['usd_value'] == 0:
                        num_instances_tx_hash_and_usd_val_is_none += 1
                else:
                    num_instances_tx_hash_is_none += 1

        labels_list = ['dex_accounts', 'gaming_accounts', 'wallet_app_accounts', 'cold_wallet_accounts', 'spam_token_deployer_accounts', 'token_contracts', 'tokenized_assets_contracts', 'dex_token_contracts', 'spam_token_contracts', 'gaming_token_contracts', 'wallet_app_token_contracts', 'account']
        # create bar chart to show number of nodes by label with matplotlib.pyplot as plt and save to file, show the labels in a key and color the bars by label. Add a key to the graph
        labels = []
        num_nodes = []
        for label in labels_list:
            labels.append(label)
            num_nodes.append(len([nd for nd in G.nodes() if G.nodes[nd]['label'] == label]))
        plt.bar(labels, num_nodes, color=['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown', 'pink'])
        plt.title('Number of nodes by label')
        plt.xlabel('Label')
        plt.ylabel('Number of nodes')
        plt.savefig('images/num_nodes_by_label.png')
    
        # heatmap of the number of edges between labels with numbers in each cell and save to file
        labels = []
        num_nodes = []
        for label in labels_list:
            labels.append(label)
            num_nodes.append(len([nd for nd in G.nodes() if G.nodes[nd]['label'] == label]))
        num_edges = []
        for label1 in labels_list:
            num_edges.append([])
            for label2 in labels_list:
                num_edges[-1].append(len([ed for ed in G.edges() if G.nodes[ed[0]]['label'] == label1 and G.nodes[ed[1]]['label'] == label2]))
        fig, ax = plt.subplots()
        im = ax.imshow(num_edges)
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax.text(j, i, num_edges[i][j], ha="center", va="center", color="w")
        ax.set_title("Number of edges between labels")
        fig.tight_layout()
        plt.savefig('images/num_edges_between_labels.png')

        # pie chart of ratio of number of num_instances_tx_hash_is_none and total_transactions
        labels = ['No Tx Hash Found', 'Total Transactions']
        sizes = [num_instances_tx_hash_is_none, total_transactions]
        explode = (0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.title('Unfound Tx Hashes vs Total Transactions')
        plt.savefig('images/ratio_num_instances_tx_hash_is_none_and_total_transactions.png')

        # pie chart of ratio of num_instances_tx_hash_and_usd_val_is_none and num_instances_tx_hash
        labels = ['Tx Hash Found and USD Value is 0', 'No Tx Hash Found']
        sizes = [num_instances_tx_hash_and_usd_val_is_none, num_instances_tx_hash]
        explode = (0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.title('Tx Hashes with 0 USD Value vs Total Tx Hashes Found')
        plt.savefig('images/ratio_num_instances_tx_hash_and_usd_val_is_none_and_num_instances_tx_hash.png')

        # chart for number of fraud accounts by label
        labels = []
        num_fraud_accounts = []
        for label in labels_list:
            labels.append(label)
            num_fraud_accounts.append(len([nd for nd in G.nodes() if G.nodes[nd]['label'] == label and G.nodes[nd]['isp'] == 1]))
        plt.bar(labels, num_fraud_accounts, color=['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown', 'pink'])
        plt.title('Number of fraud accounts by label')
        plt.xlabel('Label')
        plt.ylabel('Number of fraud accounts')
        plt.savefig('images/num_fraud_accounts_by_label.png')
        




    

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
        
