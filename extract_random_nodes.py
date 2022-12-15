# Pick up 2,230 nodes from the network, consisting of 1,165 fraud nodes and 1,165 normal nodes chosen randomly.
import datetime
import networkx as nx
import random
import numpy as np
import requests
import json
import pprint
import pandas as pd
from get_tx_hash import get_tx_hash
import asyncio
from get_tx_value import get_tx_value
from get_tx_hash_v2 import get_tx_hash_v2
from get_tx_value_v2 import get_tx_value_v2
import csv
import time
from to_iso_time import to_iso_time
from etherscan_labels import dex_accounts, gaming_accounts, wallet_app_accounts, cold_wallet_accounts, spam_token_deployer_accounts, token_contracts, tokenized_assets_contracts, dex_token_contracts, spam_token_contracts, gaming_token_contracts, wallet_app_token_contracts



def extract_random_nodes_and_label(G, n_fraud, n_normal, is_subgraph=False, preload_path=None, skipLoading=False):
    if not skipLoading:

    ######## Extract random fraud and normal nodes from the graph to create a subgraph
        if not is_subgraph:
            # pick up fraud nodes before 
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
            # remove duplicate edges
            # replace graph edges with edges  
        else:
            nodes = [nd for nd in nx.nodes(G)]

        unique_senders_receivers = {}
        overall_earliest_timestamp = 9999999999999999
        overall_latest_timestamp = 0
        print('starting')

        
        ####### OPTIONAL: Preload JSON file
        pre_loaded_json = None
        try:
            with open(preload_path) as f:
                pre_loaded_json = json.load(f)
        except:
            pre_loaded_json = None

        ####### Iterate through edges and compile unique senders, and their receivers
        if is_subgraph:
            startTime = datetime.datetime.now()
            num_edges_with_tx_hash = 0
            if not pre_loaded_json:
                idx = -1
                for edge in G.edges():
                    idx += 1
                    if idx % 1000 == 0:
                        print('processing edge: ', idx, ' of ', G.number_of_edges())
                    address_from = edge[0]
                    address_to = edge[1]
                
                    if address_from not in unique_senders_receivers:
                        unique_senders_receivers[address_from] = {
                            'receivers': [address_to],
                            'earliest_timestamp': G[address_from][address_to][0]['timestamp'],
                            'latest_timestamp': G[address_from][address_to][0]['timestamp'],
                        }
                    else:
                        unique_senders_receivers[address_from]['receivers'].append(address_to)
                        earliest_timestamp = 999999999999999999
                        latest_timestamp = 0
                        for tran in range(len(G[address_from][address_to])):
                            if G[address_from][address_to][tran]['timestamp'] < earliest_timestamp:
                                earliest_timestamp = G[address_from][address_to][tran]['timestamp']
                            if G[address_from][address_to][tran]['timestamp'] > latest_timestamp:
                                latest_timestamp = G[address_from][address_to][tran]['timestamp']
                        if earliest_timestamp < unique_senders_receivers[address_from]['earliest_timestamp']:
                            unique_senders_receivers[address_from]['earliest_timestamp'] = earliest_timestamp
                        if latest_timestamp > unique_senders_receivers[address_from]['latest_timestamp']:
                            unique_senders_receivers[address_from]['latest_timestamp'] = latest_timestamp
                        if earliest_timestamp < overall_earliest_timestamp:
                            overall_earliest_timestamp = earliest_timestamp
                        if latest_timestamp > overall_latest_timestamp:
                            overall_latest_timestamp = latest_timestamp

                print('Number of edges with tx hash: ', num_edges_with_tx_hash)
                print('Number of edges: ', G.number_of_edges())
                print('overall earliest timestamp: ', to_iso_time(overall_earliest_timestamp))
                print('overall latest timestamp: ', to_iso_time(overall_latest_timestamp))
                # save unique senders receivers to file
                with open('unique_senders_receivers_with_values.json', 'w') as fp:
                    json.dump(unique_senders_receivers, fp)
                # close file
                fp.close()

            else:
                unique_senders_receivers = pre_loaded_json
                print('loaded unique senders receivers from file')
            endTime = datetime.datetime.now()
            print('Time for extracting unique senders receivers: ', endTime - startTime)

    
        
            
            startTime = datetime.datetime.now()
            idx = -1
            startIndex = 1000
            if (startIndex < 999):
                for sender in unique_senders_receivers:
                    idx += 1
                    # skip to startIndex
                    if idx < startIndex:
                        continue

                    if (idx % 10 == 0):
                        print('processing sender: ', idx, ' of ', len(unique_senders_receivers))
                    receivers = unique_senders_receivers[sender]['receivers']
                    earliest_timestamp = unique_senders_receivers[sender]['earliest_timestamp']
                    latest_timestamp = unique_senders_receivers[sender]['latest_timestamp']
                    txns,error = get_tx_hash_v2(sender, receivers, to_iso_time(latest_timestamp+7200), to_iso_time(earliest_timestamp-7200))
                    # get transaction hashes from txns
                    transactions = []
                    if not txns:
                        txns = []
                    for txn in txns:
                        transactions.append(txn['transaction_hash'])
                    usd_values = get_tx_value_v2(transactions)
                    for i in range(len(txns)):
                        try:
                            if (txns[i]['transaction_hash'] == usd_values[i]['transaction']):
                                txns[i]['usd_value'] = abs(usd_values[i]['net_value'])
                            else:
                                txns[i]['usd_value'] = 0
                        except:
                            txns[i]['usd_value'] = 0
                    unique_senders_receivers[sender]['txns'] = txns
                    unique_senders_receivers[sender]['error'] = error
                    with open('unique_senders_receivers_with_values.json', 'w') as fp:
                        json.dump(unique_senders_receivers, fp)
                    fp.close()
                endTime = datetime.datetime.now()
                # save unique senders receivers to file

                print('Time to get unique senders receivers data: ', endTime - startTime)
                print('first object: ', unique_senders_receivers[list(unique_senders_receivers.keys())[0]], 'sender: ', list(unique_senders_receivers.keys())[0])
        print('unique senders receivers: ', len(unique_senders_receivers))
        num_tx_not_found = 0
        nodes_with_tx_hashes = 0
        error = False
        startTime = datetime.datetime.now()
        
        ####### Pull transaction data from Transpose and Lore API #######
        with open('tx2000.csv', 'w') as csvfile:
            fieldnames = ['from', 'to', 'timestamp', 'tx_hash', 'amount', 'usd_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if is_subgraph:
                for edge in G.edges():
                        index += 1
                        if index % 1000 == 0:
                            print('processing edge: ', index, ' of ', G.number_of_edges())
                        address_from = edge[0]
                        address_to = edge[1]
                        try:
                            txns = unique_senders_receivers[address_from]['txns']
                        except:
                            txns = []
                        if (len(txns) == 0):
                            continue
                        for tx in txns:
                            value = tx['value']
                            if value != 0:
                                value = value / 10**18
                            txn_timestamp = tx['timestamp']
                            timestamp_unix = datetime.datetime.fromisoformat(txn_timestamp.replace('Z', '')).timestamp()

                            found = False
                            for i in range(len(G[edge[0]][edge[1]])):
                                address_timestamp = G[address_from][address_to][i]['timestamp']
                                date_unix = datetime.datetime.fromisoformat(to_iso_time(address_timestamp).replace('Z', '')).timestamp()
                                amount = G[address_from][address_to][i]['amount']
                                if (value == amount):
                                        if (value != 0):
                                            G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                            G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                            nodes_with_tx_hashes += 1
                                            found = True
                                            writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                            break
                                        elif (abs(date_unix - timestamp_unix) < 3600):
                                            G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                            G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                            nodes_with_tx_hashes += 1
                                            found = True
                                            writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                            break
                                # if unix timestamp is past other timestamp break
                                elif (date_unix > timestamp_unix):
                                    break


        
                            
                                    
                                        





                        
                

                print('Number of transactions not found: ', num_tx_not_found, ' out of ', len(G.edges()))
                print('Number of transactions found: ',nodes_with_tx_hashes, ' out of ', len(G.edges()))
                endTime = datetime.datetime.now()
                print('Time to get tx hashes: ', endTime - startTime)
        csvfile.close()
    

        ######## Amplify missing edge data with Defillama API ########
        for edge in G.edges():
            idx += 1
            if idx % 1000 == 0:
                print('processing edge defillama: ', idx, ' of ', G.number_of_edges())
            for i in range(len(G[edge[0]][edge[1]])):
                if 'tx_hash' not in G[edge[0]][edge[1]][i]:
                    timestamp = G[edge[0]][edge[1]][i]['timestamp']
                    G[edge[0]][edge[1]][i]['tx_hash'] = 'not found'
                    value = G[edge[0]][edge[1]][i]['amount']
                    if (value != 0):
                        # sleep to avoid rate limit
                        # time.sleep(0.1)
                        try:
                            url = f'https://coins.llama.fi/prices/historical/{timestamp}/coingecko:ethereum'
                            response = requests.get(url).json()
                            price = response['coins']['coingecko:ethereum']['price']
                        except:
                            # change timestamp to int
                            timestamp = int(timestamp)
                            # change last 5 digits to 00000
                            timestamp = timestamp - (timestamp % 100000)
                            try:
                                url = f'https://coins.llama.fi/prices/historical/{timestamp}/coingecko:ethereum'
                                response = requests.get(url).json()
                                price = response['coins']['coingecko:ethereum']['price']
                            except:
                                price = 0
                        G[edge[0]][edge[1]][i]['usd_value'] = price * value
                        
                    else:
                        G[edge[0]][edge[1]][i]['usd_value'] = 0
    else:
        nodes = [nd for nd in nx.nodes(G)]
    ######### Label nodes
    labels_list = [dex_accounts, gaming_accounts, wallet_app_accounts, cold_wallet_accounts, spam_token_deployer_accounts, token_contracts, tokenized_assets_contracts, dex_token_contracts, spam_token_contracts, gaming_token_contracts, wallet_app_token_contracts]
    idx = -1
    if is_subgraph:
        for nd in nodes:
            idx += 1
            if (idx % 100 == 0):
                print('Processing nodes up to: ', idx)
            node_one_hot = [0] * len(labels_list)
            # add one to end of node_one_hot
            node_one_hot.append(1)
            G.nodes[nd]['one_hot'] = node_one_hot

            for i in range(len(labels_list)):
                if nd in labels_list[i]:
                    node_one_hot[i] = 1
                    node_one_hot[-1] = 0
                    

            node_send_num = 0
            node_receive_num = 0
            unique_accounts_sent_transactions = []
            unique_accounts_received_transactions = []
            total_amount_sent = 0
            total_amount_received = 0
            usd_sent = 0
            usd_received = 0
            for edge in G.edges(nd):
                for i in range(len(G[edge[0]][edge[1]])):
                    if edge[0] == nd:
                        node_send_num += 1
                        unique_accounts_sent_transactions = list(set(unique_accounts_sent_transactions + [edge[1]]))
                        total_amount_sent += G[edge[0]][edge[1]][i]['amount']
                        usd_sent += G[edge[0]][edge[1]][i]['usd_value']
                    else:
                        node_receive_num += 1
                        unique_accounts_received_transactions = list(set(unique_accounts_received_transactions + [edge[0]]))
                        total_amount_received += G[edge[0]][edge[1]][i]['amount']
                        usd_received += G[edge[0]][edge[1]][i]['usd_value']
            G.nodes[nd]['pagerank'] = nx.pagerank(G, alpha=0.85, personalization={nd: 1}, max_iter=1000)[nd]
            G.nodes[nd]['send_amount'] = total_amount_sent
            G.nodes[nd]['recv_amount'] = total_amount_received
            G.nodes[nd]['send_num'] = node_send_num
            G.nodes[nd]['recv_num'] = node_receive_num
            G.nodes[nd]['out_degree'] = len(unique_accounts_sent_transactions)
            G.nodes[nd]['in_degree'] = len(unique_accounts_received_transactions)
            G.nodes[nd]['send_amount_usd'] = usd_sent
            G.nodes[nd]['recv_amount_usd'] = usd_received

    ######### print statistics
    # print number of nodes and edges
    print('Number of nodes: ', len(nodes))
    print('Number of edges: ', len(G.edges(nodes)))
    # print number of fraud nodes and edges
    print('Number of fraud nodes: ', len([nd for nd in nodes if G.nodes[nd]['isp'] == 1]))
    print('Number of fraud edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 1 and G.nodes[ed[1]]['isp'] == 1]))
    # print number of normal nodes and edges
    print('Number of normal nodes: ', len([nd for nd in nodes if G.nodes[nd]['isp'] == 0]))
    print('Number of normal edges: ', len([ed for ed in G.edges(nodes) if G.nodes[ed[0]]['isp'] == 0 and G.nodes[ed[1]]['isp'] == 0]))
    # Return the subgraph
    if (is_subgraph):
        return G
    else:
        return G.subgraph(nodes)