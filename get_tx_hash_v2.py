import requests
def get_tx_hash_v2(sender, receivers, latestTimestamp, earliestTimestamp):
    # get transactions from sender
        headers = {
            'x-api-key': '0B2HufLSwgSbAzU6HSbU9gT1iBBSLyGo',
            'Content-Type': 'application/json',
        }

        json_data = {
            'sql': 'SELECT transaction_hash ,timestamp, value, from_address, to_address from ethereum.transactions  where  timestamp < \'2019-01-17\' and timestamp > \'2015-09-09\' and from_address = \'0x2343\' and to_address in (\'0x23\', \'0x493\')  ',
        }
        # replace sender and receivers
        json_data['sql'] = json_data['sql'].replace('0x2343', sender)
        json_data['sql'] = json_data['sql'].replace('2019-01-17', latestTimestamp)
        json_data['sql'] = json_data['sql'].replace('2015-09-09', earliestTimestamp)
        # replace receivers
        receivers_string = ''
        for receiver in receivers:
            receivers_string = receivers_string + '\'' + receiver + '\', '
        receivers_string = receivers_string[:-2]
        json_data['sql'] = json_data['sql'].replace('(\'0x23\', \'0x493\')', '(' + receivers_string + ')')
        


        response = requests.post('https://api.transpose.io/sql', headers=headers, json=json_data)
        response = response.json()
        error = False
        result = None
        if (response['status'] == 'error'):
            print('error: ', response)
            # convert response to string
            response = str(response)
            # if error is due to rate limit, wait 1 second and try again
            if 'credit' in response:
                error = True
        else:
            result = response['results']

        return [result, error]

        