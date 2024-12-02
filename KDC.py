# KDC (Key Distribution Center)
import socket
import json
import secrets

# Configuración
KDC_IP = "192.168.3.5"
KDC_PORT = 5555
USERS = {"clientA": "passwordA", "clientB": "passwordB"}
SESSION_KEYS = {}

def handle_request(data):
    try:
        request = json.loads(data)
        user = request["user"]
        password = request["password"]
        if user in USERS and USERS[user] == password:
            session_key = secrets.token_hex(16)
            SESSION_KEYS[user] = session_key
            print(f"User {user} authenticated successfully.")
            return json.dumps({"status": "success", "session_key": session_key})
        else:
            print(f"Failed authentication attempt for user {user}.")
            return json.dumps({"status": "error", "message": "Invalid credentials"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def start_kdc():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((KDC_IP, KDC_PORT))
        server.listen(5)
        print(f"KDC running on {KDC_IP}:{KDC_PORT}")
        while True:
            client, addr = server.accept()
            with client:
                print(f"Connection from {addr}")
                data = client.recv(1024).decode()
                response = handle_request(data)
                client.send(response.encode())

if __name__ == "__main__":
    start_kdc()
