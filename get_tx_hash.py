import requests
import datetime


def get_tx_hash(sender, receiver, date, amount):
    json_data = {
    'sql': 'SELECT transaction_hash, timestamp, value from ethereum.transactions  where      from_address = \'0x788ce285931ed095b80d75372aaa1d7d265a1aa6\'      and to_address = \'2017-11-02T07:12:11Z\'            ',
    }
    # rewrite json_data with sender and date
    json_data['sql'] = json_data['sql'].replace(
        '0x788ce285931ed095b80d75372aaa1d7d265a1aa6', sender)
    json_data['sql'] = json_data['sql'].replace('2017-11-02T07:12:11Z',receiver)
    url = 'https://sql.transpose.io/'
    # post request with query as body  and api key
    headers = {
        'x-api-key': '0B2HufLSwgSbAzU6HSbU9gT1iBBSLyGo',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json=json_data, headers=headers).json()
    error = False
    if (response['status'] == 'error'):
        print('error: ', response)
        # convert response to string
        response = str(response)
        # if error is due to rate limit, wait 1 second and try again
        if 'credit' in response:
            error = True
            tx_hash = []
        

    try:
        # if multiple transactions, add the one with the correct amount to array
        amount_correct_tx_hashes = []
        if len(response['results']) > 1 and len(response['results']) > 1 :
            for tx in response['results']:
                value = tx['value']
                # convert wei to ether
                value = value / 1000000000000000000
                if value == amount:
                    amount_correct_tx_hashes.append(tx['transaction_hash'])
        # if multiple transactions with correct amount, add the one with the correct timestamp to array
            timestamp_correct_tx_hashes = []
            if len(amount_correct_tx_hashes) > 1 or len(amount_correct_tx_hashes) == 0:
                for tx in response['results']:
                    timestamp = tx['timestamp']
                    if timestamp == date:
                        timestamp_correct_tx_hashes.append(tx['transaction_hash'])
                        break
                    # if timestamp is within 1.01 hour of date, add to array
                    # convert timestamp to unix time
                    timestamp_unix = datetime.datetime.fromisoformat(timestamp).timestamp()
                    # convert date to unix time
                    date_unix = datetime.datetime.fromisoformat(date).timestamp()
                    # if timestamp is within 1.01 hour of date, add to array
                    if timestamp_unix > date_unix - 3700 and timestamp_unix < date_unix + 3700:
                        timestamp_correct_tx_hashes.append(tx['transaction_hash'])
                        break
                    elif timestamp[0:4] == date[0:4] and timestamp[5:7] == date[5:7] and timestamp[8:10] == date[8:10] and timestamp[11:13] == date[11:13]:
                        timestamp_correct_tx_hashes.append(tx['transaction_hash'])
                if len(timestamp_correct_tx_hashes) > 1:
                    print('multiple transactions with same amount and timestamp')
                    tx_hash = timestamp_correct_tx_hashes[0]
                elif len(timestamp_correct_tx_hashes) == 0:
                    print('no transactions with same amount and timestamp')
                    tx_hash = None
                else:
                    tx_hash = timestamp_correct_tx_hashes[0]
            else:
                tx_hash = amount_correct_tx_hashes[0]


        else:
            tx_hash = response['results'][0]['transaction_hash']
    except:
        tx_hash = []
    return [tx_hash, error]
