# Uncomment this to pass the first stage
import socket
import threading 
import sys
import gzip

def handle(client):
    while True:
        chunk = client.recv(4096)
        msg = chunk.decode().split("\r\n")
        print(msg)
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        # if chunk == "":
        #     break
        #
        if msg[0].split(" ")[0] == "GET": 
            if msg[0].split(" ")[1][:6] == "/echo/":
                if "Accept-Encoding: " not in msg[-3]:
                    text = msg[0].split(" ")[1][6:]
                    response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(text)) + "\r\n\r\n" + str(text)).encode("utf-8")
                elif "Accept-Encoding: " in msg[-3]:
                    if "gzip" in msg[-3]:
                        text = msg[0].split(" ")[1][6:]
                        text = gzip.compress(text.encode())
                        # response = (f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}").encode('utf-8')
                        response = b"".join(
                            [
                            b"HTTP/1.1 200 OK",
                            b"\r\n",
                            b"Content-Encoding: gzip",
                            b"\r\n",
                            b"Content-Type: text/plain\r\n",
                            b"Content-Length: %d\r\n" % len(text),
                            b"\r\n",
                            text,
                            ]
                        )
                    else:
                        text = msg[0].split(" ")[1][6:]
                        response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(text)) + "\r\n\r\n" + str(text)).encode("utf-8")
            elif msg[0].split(" ")[1][:len("/files/")] == "/files/":
                filename = msg[0].split(" ")[1][len("/files/"):]
                try:
                    with open(("/tmp/data/codecrafters.io/http-server-tester/" + filename), "r") as file:
                        file_contents = file.readline()
                        response = ("HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+ str(len(file_contents)) +"\r\n\r\n" + file_contents).encode('utf-8')
                except:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"
            elif msg[0].split(" ")[1] == "/user-agent":
                user_agent = msg[2].split(" ")[1] 
                response = ("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(user_agent)) +"\r\n\r\n" + user_agent).encode('utf-8')
            elif msg[0].split(" ")[1] == "/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
                    
        elif msg[0].split(" ")[0] == "POST":
            if msg[0].split(" ")[1][:len("/files/")] == "/files/":
                with open(str(sys.argv[2]) + str(msg[0].split(" ")[1][len("/files/"):]), "w+") as file:
                    file.write(msg[-1])
                    response = b"HTTP/1.1 201 Created\r\n\r\n"

        client.sendall(response)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, addr = server_socket.accept() # wait for client    
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()
