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
from etherscan_labels import dex_accounts, gaming_accounts, wallet_app_accounts, cold_wallet_accounts, spam_token_deployer_accounts, token_contracts, tokenized_assets_contracts, dex_token_contracts, spam_token_contracts, gaming_token_contracts, wallet_app_token_contracts

def to_iso_time(timestamp):
    iso_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            # add 4 hours to get UTC time
    iso_time = datetime.datetime.fromisoformat(iso_time) + datetime.timedelta(hours=5)
            # replace space with T and add Z to end
    iso_time = iso_time.isoformat().replace(' ', 'T') + 'Z'
    return iso_time
def extract_random_nodes_and_label(G, n_fraud, n_normal, is_subgraph=False):
    # Pick up fraud nodes
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
    # num of edges with tx hash
    
    pre_loaded_json = None
    try:
        with open('./unique_senders_receivers.json') as f:
            pre_loaded_json = json.load(f)
    except:
        pre_loaded_json = None
    
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
            print('unique senders receivers: ', len(unique_senders_receivers))
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
                # print('usd values: ', usd_values)
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



    labels_list = [dex_accounts, gaming_accounts, wallet_app_accounts, cold_wallet_accounts, spam_token_deployer_accounts, token_contracts, tokenized_assets_contracts, dex_token_contracts, spam_token_contracts, gaming_token_contracts, wallet_app_token_contracts]


    num_tx_not_found = 0
    nodes_with_tx_hashes = 0
    error = False
    # iterate through edges don't double count
    checked_edges = []
    index = -1
    # print num of edges with tx hash
    startTime = datetime.datetime.now()

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
                    for i in range(len(G[edge[0]][edge[1]])):
                        address_from = edge[0]
                        address_to = edge[1]
                        address_timestamp = G[address_from][address_to][i]['timestamp']
                        amount = G[address_from][address_to][i]['amount']
                        # check if edge has been checked
                        if (address_from, address_to, address_timestamp, amount) in checked_edges:
                            continue
                        checked_edges.append((address_from, address_to, address_timestamp, amount))
                        # make sure to only send 3 requests per second
                        # if no tx hash for edge, try to get one
                        has_tx_hash = False
                        try:
                            has_tx_hash = G[address_from][address_to][i]['tx_hash']
                            has_tx_hash = True
                            nodes_with_tx_hashes += 1
                        except:
                            pass
                        if not has_tx_hash and not error:
                            # getting tx hash
                            for tx in txns:
                                value = tx['value']
                                if value != 0:
                                    value = value / 10**18
                                txn_from = tx['from_address']
                                txn_to = tx['to_address']
                                txn_timestamp = tx['timestamp']

                                date_unix = datetime.datetime.fromisoformat(to_iso_time(address_timestamp).replace('Z', '')).timestamp()
                                timestamp_unix = datetime.datetime.fromisoformat(txn_timestamp.replace('Z', '')).timestamp()
                                # print(
                                #     'txinfo',
                                #     date_unix, timestamp_unix, to_iso_time(address_timestamp), txn_timestamp, address_from, txn_from, address_to, txn_to, value, amount, amount == value
                                # )
                                found = False
                                if (value == amount):
                                    if (value != 0):
                                        G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                        G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                        nodes_with_tx_hashes += 1
                                        found = True
                                        writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                        break
                                    # find the closest timestamp
                                    elif txn_timestamp > to_iso_time(address_timestamp):
                                        G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                        G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                        nodes_with_tx_hashes += 1
                                        found = True
                                        writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                        break
                                    elif txn_timestamp == to_iso_time(address_timestamp):
                                        G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                        G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                        nodes_with_tx_hashes += 1
                                        found = True
                                        writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                        break
                                    elif date_unix > timestamp_unix - 3700 or date_unix < timestamp_unix + 3700:
                                        G[address_from][address_to][i]['tx_hash'] = tx['transaction_hash']
                                        G[address_from][address_to][i]['usd_value'] = tx['usd_value']
                                        nodes_with_tx_hashes += 1
                                        writer.writerow({'from': address_from, 'to': address_to, 'timestamp': address_timestamp, 'tx_hash': tx['transaction_hash'], 'amount': amount, 'usd_value': tx['usd_value']})
                                        found = True
                                        break
                                # if no tx hash found, set tx_hash to 'not found'
                                if not found:
                                    G[address_from][address_to][i]['tx_hash'] = 'not found'
                                    num_tx_not_found += 1

            

            print('Number of transactions not found: ', num_tx_not_found, ' out of ', len(G.edges()))
            print('Number of transactions found: ',nodes_with_tx_hashes, ' out of ', len(G.edges()))
            endTime = datetime.datetime.now()
            print('Time to get tx hashes: ', endTime - startTime)

   

    
    csvfile.close()

            


    
    # Label nodes

    idx = 0
    if is_subgraph:
        for nd in nodes:
            node_one_hot = [0] * len(labels_list)
            # add one to end of node_one_hot
            node_one_hot.append(1)
            G.nodes[nd]['one_hot'] = node_one_hot

            node_send_num = 0
            node_receive_num = 0
            unique_accounts_sent_transactions = []
            unique_accounts_received_transactions = []
            total_amount_sent = 0
            total_amount_received = 0

            if (idx % 1000 == 0):
                print('Processing nodes up to: ', idx)

            idx += 1
            for edge in G.edges(nd):
                if edge[0] == nd:
                    node_send_num += 1
                    unique_accounts_sent_transactions = list(set(unique_accounts_sent_transactions + [edge[1]]))
                    total_amount_sent += G[edge[0]][edge[1]][0]['amount']
                else:
                    node_receive_num += 1
                    unique_accounts_received_transactions = list(set(unique_accounts_received_transactions + [edge[0]]))
                    total_amount_received += G[edge[0]][edge[1]][0]['amount']
            # calclate simple page rank
            # G.nodes[nd]['pagerank'] = nx.pagerank(G, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='amount', dangling=None)[nd]
            G.nodes[nd]['send_amount'] = total_amount_sent
            G.nodes[nd]['recv_amount'] = total_amount_received
            G.nodes[nd]['send_num'] = node_send_num
            G.nodes[nd]['recv_num'] = node_receive_num
            G.nodes[nd]['out_degree'] = len(unique_accounts_sent_transactions)
            G.nodes[nd]['in_degree'] = len(unique_accounts_received_transactions)


    
    
        




    # print num of nodes and edges

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