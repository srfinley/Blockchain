# a REPL for checking the wallets of the crypto users
import sys
import requests


if __name__ == '__main__':
    # What is the server address? IE `python3 wallet.py https://server.com/
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    r = requests.get(url=node + "/chain")

    chain = r.json()

    user = input()
    total = 0

    for block in chain['chain']:
        acts = block['transactions']
        for act in acts:
            if act['sender'] == user or act['recipient'] == user:
                # print("found s-f's transaction")
                if act['sender'] == user:
                    total -= act['amount']
                if act['recipient'] == user:
                    total += act['amount']
    print(total)
