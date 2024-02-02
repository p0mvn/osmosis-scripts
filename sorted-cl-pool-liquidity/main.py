import requests
from decimal import Decimal

# RPC endpoint URL of the Cosmos node you want to query
api_url = "https://lcd.osmosis.zone"

# Construct the URL for querying the account
account_url = f"{api_url}/osmosis/poolmanager/v1beta1/all-pools"

class Pool:
    def __init__(self, pool_id, liquidity_str):
        self.pool_id = pool_id
        self.liquidity = Decimal(liquidity_str)


pools = [];

try:
    # Send a GET request to the Cosmos REST API
    response = requests.get(account_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        pools_data = response.json()
        for pool_entry in pools_data['pools']:

            if pool_entry['@type'] != "/osmosis.concentratedliquidity.v1beta1.Pool":
                continue

            # Create a Pool object and add it to the list
            pool = Pool(pool_entry['id'], pool_entry['current_tick_liquidity'])
            pools.append(pool)
    else:
        print(f"Failed to query account. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

# Sort the pools by liquidity in descending order
sorted_pools = sorted(pools, key=lambda pool: pool.liquidity, reverse=True)

# Print the sorted pools
for pool in sorted_pools:
    print(f"Pool ID: {pool.pool_id}, Liquidity: {pool.liquidity}")
