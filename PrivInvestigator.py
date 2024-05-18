#!/usr/bin/env python3
import argparse
import requests
import json
from getpass import getpass

# Create a session
session = requests.Session()

# Global variables to store email and API keys
email = None
dehashed_api_key = None
snusbase_api_key = None
leakosint_token = None

def query_dehashed(query, size):
    headers = {
        'Accept': 'application/json',
    }
    try:
        response = session.get(
            f'https://api.dehashed.com/search?query={query}&size={size}',
            auth=(email, dehashed_api_key),
            headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None
    return response.json()

def query_snusbase(query):
    headers = {
        'Auth': snusbase_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'terms': [query],
        'types': ['email', 'username', 'password', 'name', 'hash'],  # Limit the types of data to search for
        'wildcard': False
    }
    try:
        response = session.post(
            'https://api-experimental.snusbase.com/data/search',
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        print(response.text)  # Print the full response
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None
    return response.json()

def query_leakosint(query):
    data = {
        'token': leakosint_token,
        'request': query,
        'limit': 100,
        'lang': 'en'
    }
    url = 'https://server.leakosint.com/'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None
    return response.json()

def record_input(query):
    with open('input_record.txt', 'a') as f:
        f.write(f"Email: {email}\n")
        f.write(f"Dehashed API Key: {dehashed_api_key}\n")
        f.write(f"Snusbase API Key: {snusbase_api_key}\n")
        f.write(f"LeakOsint Token: {leakosint_token}\n")
        f.write(f"Query: {query}\n")
        f.write("\n")

def send_to_discord(webhook_url, content):
    data = {
        'content': content[:2000]  # Discord's character limit
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    if len(content) > 2000:
        return send_to_discord(webhook_url, content[2000:])  # Recursively send remaining content
    return response

def logout():
    global email, dehashed_api_key, snusbase_api_key, leakosint_token
    email = None
    dehashed_api_key = None
    snusbase_api_key = None
    leakosint_token = None
    print("You have been logged out.")

def main():
    global email, dehashed_api_key, snusbase_api_key, leakosint_token

    # Check if email and API keys are already set
    if email is None or dehashed_api_key is None or snusbase_api_key is None or leakosint_token is None:
        email = input("Enter your email: ")
        dehashed_api_key = getpass("Enter your Dehashed API key: ")
        snusbase_api_key = getpass("Enter your Snusbase API key: ")
        leakosint_token = getpass("Enter your LeakOsint token: ")

    webhook_url = input("Enter your Discord webhook URL: ")

    while True:
        query = input("Enter your query (or 'quit' to stop): ")
        if query.lower() == 'quit':
            break
        elif query.lower() == 'logout':
            logout()
            continue

        # Record the input data
        record_input(query)

        print("Searching Dehashed...")
        dehashed_results = query_dehashed(query, 10000)
        if dehashed_results is not None:
            dehashed_results_str = json.dumps(dehashed_results, indent=4)
            print(dehashed_results_str)
            send_to_discord(webhook_url, f"PriveYe results for query '{query}':\n{dehashed_results_str}")

        print("Searching Snusbase...")
        snusbase_results = query_snusbase(query)
        if snusbase_results is not None:
            snusbase_results_str = json.dumps(snusbase_results, indent=4)
            print(snusbase_results_str)
            send_to_discord(webhook_url, f"PriveYe results for query '{query}':\n{snusbase_results_str}")

        print("Searching LeakOsint...")
        leakosint_results = query_leakosint(query)
        if leakosint_results is not None:
            leakosint_results_str = json.dumps(leakosint_results, indent=4)
            print(leakosint_results_str)
            send_to_discord(webhook_url, f"PriveYe results for query '{query}':\n{leakosint_results_str}")

if __name__ == "__main__":
    main()
