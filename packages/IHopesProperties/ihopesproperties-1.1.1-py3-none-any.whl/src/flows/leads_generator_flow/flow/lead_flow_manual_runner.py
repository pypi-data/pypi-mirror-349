from typing import List

from flows.leads_generator_flow.flow.lead_flow import address_based_lead_flow
from google_drive.authenticator import get_google_services

if __name__ == '__main__':

    addresses: List[str] = [
        '211 Ohio St, Monroeville, PA 15146',
    ]

    print('Authenticating...')
    get_google_services()
    print('Authenticated successfully.')

    for address in addresses:
        print(f'Working on address: {address}')
        address_based_lead_flow(address=address)
