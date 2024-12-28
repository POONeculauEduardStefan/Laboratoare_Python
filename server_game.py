# server.py
import socket
import threading

def handle_client(conn, addr, player_id, active_clients):
    print(f"Conexiune acceptată de la {addr} - Player {player_id}")
    while True:
        try:
            # Primește mesajul de la client
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode()
            print(f"Primit de la Player {player_id} ({addr}): {message}")

            # Verifică dacă mesajul este "exit"
            if message.lower() == "exit":
                print(f"Conexiunea cu Player {player_id} ({addr}) a fost închisă. O zi frumoasă!")
                conn.send("O zi frumoasă!".encode())
                break

            # Trimite un răspuns clientului
            response = f"Serverul a primit mesajul de la Player {player_id}: {message}"
            conn.send(response.encode())
        except ConnectionResetError:
            break

    conn.close()
    active_clients.remove(player_id)
    print(f"Player {player_id} a fost deconectat. Clienți activi: {len(active_clients)}")

def reject_client(conn, addr):
    print(f"Conexiune refuzată de la {addr}: Serverul este plin.")
    try:
        conn.send("Serverul este plin. Încearcă mai târziu.".encode())
    except Exception as e:
        print(f"Eroare la trimiterea mesajului către client: {e}")
    finally:
        conn.close()

def start_server():
    host = '127.0.0.1'  # Adresa IP a serverului (localhost)
    port = 65432         # Portul pe care serverul ascultă

    # Creare socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Ascultă conexiuni (maxim 5 în coadă)
    print(f"Server pornit pe {host}:{port}")

    threads = []
    active_clients = set()
    player_id = 1

    try:
        while True:
            conn, addr = server_socket.accept()  # Acceptă conexiunea de la client

            if len(active_clients) < 2:
                conn.send("Mai este loc in server".encode())
                active_clients.add(player_id)
                client_thread = threading.Thread(target=handle_client, args=(conn, addr, player_id, active_clients))
                client_thread.start()
                threads.append(client_thread)
                print(f"Player {player_id} s-a conectat.")
                player_id += 1
            else:
                reject_client(conn, addr)

    finally:
        for thread in threads:
            thread.join()
        server_socket.close()
        print("Serverul s-a oprit")

if __name__ == "__main__":
    start_server()
