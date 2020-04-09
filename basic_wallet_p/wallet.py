# a REPL for checking the wallets of the crypto users
import sys
import requests

from colorama import init, Fore, Back, Style


def transact(node, sender, recipient, amount):
    endpoint = f"{node}/transactions/new"

    post_data = {
        'sender': sender,
        'recipient': recipient,
        'amount': int(amount)
    }

    r = requests.post(url=endpoint, json=post_data)
    return r


if __name__ == '__main__':
    init()
    # What is the server address? IE `python3 wallet.py https://server.com/
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    print("Welcome to the Salambdacoin wallet!")
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
                        print(f"{user} sent {Fore.RED}{act['amount']}{Style.RESET_ALL} to {act['recipient']}")
                        total -= act['amount']
                    if act['recipient'] == user:
                        print(f"{user} received {Fore.GREEN}{act['amount']}{Style.RESET_ALL} from {act['sender']}")
                        total += act['amount']
        print(f"{user} has {Back.GREEN}{total}{Style.RESET_ALL} Salambdacoins.")
        print("To make another query, enter a username.")
        print("To exit, enter 'x'")
        print("To make a transaction, enter 'transaction'")
        user = input()
        if user == 'x':
            break
        if user == 'transaction':
            print("Sending user:")
            sender = input()
            print("Receiving user:")
            recipient = input()
            print("Amount:")
            amount = input()
            print(f"Sending {amount} from {sender} to {recipient}...")
            r = transact(node, sender, recipient, amount)
            print(f"{Back.GREEN}{r.json()['message']}{Style.RESET_ALL}")
            print(f"Let's see if {recipient} has received it yet.")
            user = recipient
