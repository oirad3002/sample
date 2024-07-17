
import requests
import json
from typing import List, Tuple

# TODO: Keep up to date!
DEVICE_NAME_LUT = {
    # MAC address        # Description
    'd0:9f:d9:40:e3:41': 'CAG A  Skytower Prd',
    'd0:9f:d9:40:e3:b9': 'CAG A  Skytower Stg',
    'd0:9f:d9:40:e3:49': 'CAG K3 Freight Prd',
    'd0:9f:d9:40:e3:cf': 'CAG K3 Freight Stg',
    'd0:9f:d9:41:04:62': 'CAG K4 Prd',
    'd0:9f:d9:40:ff:9a': 'CAG K4 Test',
    'd0:9f:d9:40:ea:35': 'CAG K4 Stg',
    'd0:9f:d9:41:04:60': 'Hamburg',
    'd0:9f:d9:41:7f:b5': 'TEST ASIA PACIFIC',
    'd0:9f:d9:41:04:12': 'CHRIS',
    'd0:9f:d9:41:03:74': 'TEST INTERNATIONAL'
}
URL     = 'https://elevate.access.cedes-connect.com/admin'
HEADERS = { 'X-API-Token': 'VPVdOvzVBhfxTWWOkVykaGhUigzabEIU' }

def descr_and_ip_list() -> List[Tuple[str, str]]:
    result = []

    response = requests.get(URL, headers=HEADERS)
    response_json = response.json()

    for item in response_json['data']:
        json_data = json.loads(item['jsondata'].replace("'", '"'))
        mac_addr = json_data['macID']
        if mac_addr in DEVICE_NAME_LUT:
            ip_addr = item["ipv4"]
            result.append((DEVICE_NAME_LUT.get(mac_addr), ip_addr))
    return result

def print_descr_and_ip_list() -> None:
    print('\n'.join([f'{descr:32s} {ip}' for descr, ip in descr_and_ip_list()]))

def print_descr_and_ssh_cmd_list() -> None:
    print('\n'.join([f'{descr:32s} ssh -i ~/.ssh/cedes_id_ecdsa -p 3791 -J remoteaccess@cedes.connect.relayr.io -l cedes -- {ip}' for descr, ip in descr_and_ip_list()]))
    # print('\n'.join([f'{descr:32s} ssh -i ~/.ssh/cedes_id_ecdsa -p 3791 -J remoteaccess@elevate.access.cedes-connect.com -l cedes -- {ip}' for descr, ip in descr_and_ip_list()]))

def print_upload_commands(src: str, dst: str) -> None:
    print('\n'.join([f'scp -P 3791 -J remoteaccess@elevate.access.cedes-connect.com -i ~/.ssh/cedes_id_ecdsa -r {src} cedes@{ip}:{dst}' for _, ip in descr_and_ip_list()]))

def print_download_commands(src: str, dst: str) -> None:
    print('\n'.join([f'scp -P 3791 -J remoteaccess@elevate.access.cedes-connect.com -i ~/.ssh/cedes_id_ecdsa cedes@{ip}:{src} {dst}' for _, ip in descr_and_ip_list()]))

if __name__ == '__main__':
    print_descr_and_ssh_cmd_list()
    # print_upload_commands('C:/_work/219_cegard_Smart_MVP_System/219_python_scripts/test.txt', '~')
    # print_download_commands('~/test.txt', 'C:/_work/219_cegard_Smart_MVP_System/219_python_scripts')