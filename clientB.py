import socket
import json

CLIENT_B_IP = "192.168.1.11"
CLIENT_B_PORT = 5556  # Puerto personalizado para sincronización con el KDC
KDC_IP = "192.168.1.10"
KDC_PORT = 5555
VALID_SESSION_KEYS = []

def sync_with_kdc():
    """Sincroniza las claves válidas con el KDC."""
    global VALID_SESSION_KEYS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((KDC_IP, KDC_PORT))
        request = json.dumps({"action": "get_valid_keys"})
        client.send(request.encode())
        response = client.recv(1024).decode()
        data = json.loads(response)
        if data["status"] == "success":
            VALID_SESSION_KEYS = data["valid_keys"]
            print("Claves sincronizadas con éxito:", VALID_SESSION_KEYS)
        else:
            print("Error al sincronizar claves con el KDC:", data["message"])

def handle_connection(session_key):
    """Valida claves de sesión enviadas por el cliente SSH."""
    if session_key in VALID_SESSION_KEYS:
        return "Session validated. Communication accepted."
    else:
        return "Invalid session key."

def start_client_b():
    """Inicia el servicio que escucha claves desde el KDC."""
    sync_with_kdc()  # Sincronización inicial
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((CLIENT_B_IP, CLIENT_B_PORT))
        server.listen(5)
        print(f"Client B running on {CLIENT_B_IP}:{CLIENT_B_PORT}")
        while True:
            client, addr = server.accept()
            with client:
                print(f"Connection from {addr}")
                data = client.recv(1024).decode()
                response = handle_connection(data)
                client.send(response.encode())

if __name__ == "__main__":
    start_client_b()
