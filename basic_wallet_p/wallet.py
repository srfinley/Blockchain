# a REPL for checking the wallets of the crypto users
import sys
import requests


if __name__ == '__main__':
    # What is the server address? IE `python3 wallet.py https://server.com/
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    print("Welcome to the Lambdacoin wallet!")
    print("For which user would you like wallet information?")
    user = input()
    while True:
        print("Running a fresh query to get you the latest information...")
        r = requests.get(url=node + "/chain")
        chain = r.json()

        total = 0

        for block in chain['chain']:
            acts = block['transactions']
            for act in acts:
                if act['sender'] == user or act['recipient'] == user:
                    if act['sender'] == user:
                        print(f"{user} sent {act['amount']} to {act['recipient']}")
                        total -= act['amount']
                    if act['recipient'] == user:
                        print(f"{user} received {act['amount']} from {act['sender']}")
                        total += act['amount']
        print(f"{user} has {total} Lambdacoins.")
        print("To make another query, enter a username.")
        print("To exit, enter 'x'")
        user = input()
        if user == 'x':
            break
