import socket
import json
import paramiko

KDC_IP = "192.168.3.5"
KDC_PORT = 5555
CLIENT_B_IP = "192.168.1.11"
CLIENT_B_PORT = 22  # Puerto estándar para SSH

def request_ticket(user, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((KDC_IP, KDC_PORT))
        request = json.dumps({"user": user, "password": password})
        client.send(request.encode())
        response = client.recv(1024).decode()
        return json.loads(response)

def communicate_with_client_b_ssh(session_key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(CLIENT_B_IP, username="clientB", password=session_key)

    # Ejecuta un comando remoto o envía datos
    stdin, stdout, stderr = ssh.exec_command("echo 'Session key validated via SSH'")
    print(stdout.read().decode())
    ssh.close()

if __name__ == "_main_":
    user = "clientA"
    password = "passwordA"
    ticket = request_ticket(user, password)
    
    if ticket["status"] == "success":
        print("Authenticated successfully!")
        print(f"Received Ticket: {ticket}")  # Muestra el ticket completo
        communicate_with_client_b_ssh(ticket["session_key"])
    else:
        print("Authentication failed:", ticket["message"])