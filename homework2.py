#question 1
#server code

import socket
import threading

# Bank account details
accounts = {
    '1357': 1000,
    '2468': 500
}


def handle_client(client_socket):
    account_number = client_socket.recv(1024).decode()
    if account_number in accounts:
        client_socket.send(b"Welcome! you connected to bank server.")
    else:
        client_socket.send(b"Invalid account number. Connection terminated.")
        client_socket.close()
        return

    while True:
        option = client_socket.recv(1024).decode()

        if option == '1':
            balance = accounts[account_number]
            client_socket.send(f"Your current balance is: {balance}".encode())
        elif option == '2':
            amount = int(client_socket.recv(1024).decode())
            accounts[account_number] += amount
            client_socket.send(f"Deposit successful. Your new balance is: {accounts[account_number]}".encode())
        elif option == '3':
            amount = int(client_socket.recv(1024).decode())
            if accounts[account_number] >= amount:
                accounts[account_number] -= amount
                client_socket.send(f"Withdrawal successful. Your new balance is: {accounts[account_number]}".encode())
            else:
                client_socket.send("Insufficient funds. Withdrawal failed.".encode())
        else:
            break

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))
    server.listen(5)
    print("Server listening on port 12345...")

    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address} established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


start_server()



#client code 

import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))

    account_number = input("Enter your account number: ")
    client.send(account_number.encode())

    print(client.recv(1024).decode())

    while True:
        print("\nOptions:")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        option = input("Enter option: ")

        if option == '4':
            break

        client.send(option.encode())

        if option == '1':
            print(client.recv(1024).decode())
        elif option == '2' or option == '3':
            amount = input("Enter amount: ")
            client.send(amount.encode())
            print(client.recv(1024).decode())

    client.close()


if __name__ == "__main__":
    main()
    
    
    
#question 2 

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("first.html")

@app.route('/location.html')
def about():
    return render_template("location.html")
@app.route('/opinion.html')
def contacts():
    return render_template("opinion.html")

if __name__ == "__main__":
    app.run(debug = True)