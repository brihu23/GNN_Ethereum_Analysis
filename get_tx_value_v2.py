import requests
def get_tx_value_v2(tx_hashs):
    api_url = f'https://www.app.lorescan.com/api/transaction/decoded0?chain=1'
    # api_url = f'http://localhost:3000/api/transaction/decoded0?chain=1'
    json_data = {
        'transactions': tx_hashs
    }
    try:
        response = requests.post(api_url, json=json_data).json()
        return response
    except:
        return []
    

