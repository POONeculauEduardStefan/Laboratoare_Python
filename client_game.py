# client.py
import socket

def start_client():
    host = '127.0.0.1'  # Adresa IP a serverului (localhost)
    port = 65432         # Portul serverului

    # Creare socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))  # Se conectează la server
        print(f"Conectat la serverul de pe {host}:{port}")

        while True:
            # Primește răspunsul de la server înainte de a cere input
            response = client_socket.recv(1024).decode()
            print(response)

            # Verifică dacă răspunsul indică deconectarea sau refuzul
            if "O zi frumoasă!" in response:
                print("Serverul a închis conexiunea. O zi frumoasă!")
                break
            elif "Serverul este plin" in response:
                print("Serverul este plin. Clientul se va închide.")
                break

            # Introducerea mesajului de trimis către server
            message = input("Trimite un mesaj la server (sau 'exit' pentru a ieși): ")

            # Trimite mesajul la server
            client_socket.send(message.encode())

    except ConnectionRefusedError:
        print("Conexiunea a fost refuzată de server. Serverul este plin.")
    finally:
        client_socket.close()
        print("Clientul s-a închis.")

if __name__ == "__main__":
    start_client()
