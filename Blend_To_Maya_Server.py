import socket
import threading
import traceback
import maya.cmds as cmds
import maya.utils as utils


def handle_client(client_socket, addr):
    try:
        command = client_socket.recv(1024).decode('utf-8')

        try:
            # Execute the received command
            exec(command)
        except Exception as e:
            # Send back any errors
            client_socket.sendall(str(e).encode('utf-8'))
        else:
            # Or confirm successful execution
            client_socket.sendall("Command executed successfully.".encode('utf-8'))

    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen()

    print("Server is listening...")


    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr} has been established.")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

    finally:
        server_socket.close()

def run_server():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

def mayaFbxImport(path):
    utils.executeDeferred(lambda: cmds.file(path, i=True, type="FBX", options="fbx"))

if __name__ == "__main__":
    run_server()