import requests
import config
from logs import logger
from fastapi import HTTPException, status

def dr_reload():
    headers = { 'Content-Type' : 'application/json' }
    json_data = f'{{"jsonrpc":"2.0","method":"dr_reload","id":10}}'
    try:
        r = requests.post(config.opensips_mi_url, data=json_data, headers=headers)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unable to connect to mi interface')
    if r.json()['result'] != "OK" :
        return False
    return True