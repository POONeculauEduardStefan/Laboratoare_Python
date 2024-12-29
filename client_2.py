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
            # Primește mesaj de la server
            response = client_socket.recv(1024).decode()

            # Descompune răspunsul dacă există mai multe părți
            if response.startswith("TABLA"):
                parts = response.split("\n", 1)
                if len(parts) > 1:
                    print("Tabla de joc actuală:")
                    print(parts[1])
                continue

            # Afișează alte mesaje de la server
            print(response)

            # Dacă jocul s-a terminat sau conexiunea este refuzată, ieșim
            if "Ai câștigat!" in response or "Ai pierdut." in response or "Serverul este plin" in response:
                break

            # Dacă este rândul jucătorului, trimite mutarea
            if "E rândul tău" in response:
                while True:
                    try:
                        col = input("Introdu o coloană (0-6): ")
                        client_socket.send(col.encode())
                        break
                    except ValueError:
                        print("Te rog introdu un număr valid între 0 și 6.")

    except ConnectionRefusedError:
        print("Conexiunea a fost refuzată de server.")
    finally:
        client_socket.close()
        print("Clientul s-a închis.")

if __name__ == "__main__":
    start_client()
