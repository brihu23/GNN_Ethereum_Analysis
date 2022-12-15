import requests
def get_tx_value(tx_hash):
    api_url = f'https://app.lorescan.com/api/transaction/{tx_hash}?chain=1'
    try:
        response = requests.get(api_url).json()
        usd_net = response['finalOutput']['transactionNetValue']
    except:
        usd_net = 0
    return usd_net
    

